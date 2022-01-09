from ursina import *
import math

from weapons.sword import Sword
from weapons.shield import Shield
from weapons.bow import Bow
from weapons.arrow import Arrow

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

class Player(Entity):
    def __init__(self, position, map, speed = 2, jump_height = 0.3, controls = "wasd"):
        super().__init__(
            model = "cube", 
            position = position,
            scale = (1.3, 1, 1.3), 
            visible_self = False,
            tag = "player",
            collider = "box"
        )

        self.collider = BoxCollider(self, center = Vec3(0, 1, 0), size = Vec3(1, 1, 1))
        mouse.locked = True
        camera.parent = self
        camera.position = (0, 2, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 100
        self.velocity_x, self.velocity_y, self.velocity_z = (0, 0, 0)
        self.speed = speed
        self.jump_count = 0
        self.jump_height = jump_height
        self.slope = 10000000000000000
        self.controls = controls
        self.sensitivity = 80
        self.health = 5
        self.kills = 0
        self.sword = None
        self.bow = None
        self.arrow = None
        self.blocking = False
        self.crosshair = Entity(model = "quad", color = color.black, parent = camera, position = (0, 0, 1), scale = (0.01, 0.01, 0.01))

        self.map = map

        self.terrain = self.map.terrain

        self.sword = Sword(terrain = self.terrain)
        self.bow = Bow(terrain = self.terrain)
        self.arrow = Arrow()
        self.shield = Shield(terrain = self.terrain)

        self.sword.player = self
        self.sword.bow = self.bow
        self.sword.arrow = self.arrow
        self.sword.shield = self.shield

        self.bow.player = self
        self.bow.sword = self.sword
        self.bow.arrow = self.arrow
        self.bow.shield = self.shield
        
        self.shield.player = self
        self.shield.bow = self.bow
        self.shield.sword = self.sword
        self.shield.arrow = self.arrow

    def jump(self):
        self.velocity_y = self.jump_height * 40
        self.jump_count += 1

    def update(self):
        if self.health <= 0:
            self.disable()
            EditorCamera()
            self.sword.disable()
            self.bow.disable()
            self.arrow.disable()

        self.direction = Vec3(self.forward * (held_keys["w"] - held_keys["s"]) + self.right * (held_keys["d"] - held_keys["a"])).normalized()

        if self.sword.equipped == True and self.shield.equipped == False:
            self.sword.always_on_top = True
            self.shield.always_on_top = False
        if self.shield.equipped == True and self.sword.equipped == False:
            self.shield.always_on_top = True
            self.sword.always_on_top = False
        if self.shield.equipped == True and self.sword.equipped == True:
            self.sword.always_on_top = False
            self.shield.always_on_top = True
        if self.bow.equipped == True:
            self.bow.always_on_top = True
            self.shield.always_on_top = False
            self.sword.always_on_top = False
    
        y_movement = self.velocity_y * time.dt

        direction = (0, sign(y_movement), 0)

        x_movement = (self.forward[0] * held_keys[self.controls[0]] + 
            self.left[0] * held_keys[self.controls[1]] + 
            self.back[0] * held_keys[self.controls[2]] + 
            self.right[0] * held_keys[self.controls[3]]) * time.dt * 6 * self.speed

        z_movement = (self.forward[2] * held_keys[self.controls[0]] +
            self.left[2] * held_keys[self.controls[1]] +
            self.back[2] * held_keys[self.controls[2]] +
            self.right[2] * held_keys[self.controls[3]]) * time.dt * 6 * self.speed

        hill_ray = raycast(origin = self.position, direction = self.down, distance = 2, ignore = [self, ])

        if hill_ray.entity and hill_ray.entity.tag == "sornhill" or hill_ray.entity and hill_ray.entity.tag == "sorntop":
            yRay = boxcast(origin = self.world_position, direction=direction,
                        distance=self.scale_y/2+abs(y_movement), ignore=[self, ])
            
            if yRay.hit:
                self.jump_count = 0
                self.velocity_y = 0
            else:
                self.y += y_movement
                self.velocity_y -= 1 * time.dt * 25

            if x_movement != 0:
                direction = (sign(x_movement), 0, 0)
                x_ray = boxcast(origin=self.world_position, direction=direction,
                            distance=self.scale_x/2+abs(x_movement), ignore=[self, ],thickness = (1,1))

                if not x_ray.hit:
                    self.x += x_movement
                else:
                    top_x_ray = raycast(origin=self.world_position-(0, self.scale_y/2-.1, 0),
                                    direction=direction,distance = self.scale_x/2+math.tan(math.radians(self.slope))*.1, 
                                    ignore=[self, ])

                    if not top_x_ray.hit:
                        self.x += x_movement
                        height_ray = raycast(origin=self.world_position+(sign(x_movement)*self.scale_x/2, -self.scale_y/2, 0),
                                            direction=(0,1,0), ignore=[self, ])
                        if height_ray.hit :
                            self.y += height_ray.distance

            if z_movement != 0:
                direction = (0, 0, sign(z_movement))
                z_ray = boxcast(origin=self.world_position, direction=direction,
                            distance=self.scale_z/2+abs(z_movement), ignore=[self, ],thickness = (1,1))

                if not z_ray.hit:
                    self.z += z_movement
                else:
                    top_z_ray = raycast(origin=self.world_position-(0, self.scale_y/2-.1, 0),
                                    direction=direction,distance = self.scale_z/2+math.tan(math.radians(self.slope))*.1, 
                                    ignore=[self, ])

                    if not top_z_ray.hit:
                        self.z += z_movement
                        height_ray = raycast(origin=self.world_position+(0, -self.scale_y/2, sign(z_movement)*self.scale_z/2),
                                        direction=(0,1,0), ignore=[self, ])
                        if height_ray.hit :
                            self.y += height_ray.distance

        else:
            yRay = terraincast(origin = self.world_position, terrain = self.terrain, direction=direction, distance = self.scale_y + abs(y_movement))
        
            if yRay.hit:
                self.jump_count = 0
                self.velocity_y = 0
            else:
                self.y += y_movement
                self.velocity_y -= 1 * time.dt * 25

            if x_movement != 0:
                direction = (sign(x_movement), 0, 0)
                x_ray = terraincast(origin = self.world_position, terrain = self.terrain, direction = direction, distance = self.scale_x + abs(x_movement))

                if not x_ray.hit:
                    self.x += x_movement
                else:
                    top_x_ray = terraincast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), terrain = self.terrain, direction = direction, distance = self.scale_x + math.tan(math.radians(self.slope)))

                    if not top_x_ray.hit:
                        self.x += x_movement
                        height_ray = terraincast(origin = self.world_position + (sign(x_movement) * self.scale_x / 2, -self.scale_y / 2, 0), terrain = self.terrain, direction = (0, 1, 0))
                        if height_ray.hit:
                            self.y += height_ray.distance / 5

            if z_movement != 0:
                direction = (0, 0, sign(z_movement))
                z_ray = terraincast(origin = self.world_position, terrain = self.terrain, direction = direction, distance = self.scale_z + abs(z_movement))

                if not z_ray.hit:
                    self.z += z_movement
                else:
                    top_z_ray = terraincast(origin = self.world_position - (0, self.scale_y / 2 -0.1, 0), terrain = self.terrain, direction = direction, distance = self.scale_z + math.tan(math.radians(self.slope)))

                    if not top_z_ray.hit:
                        self.z += z_movement
                        height_ray = terraincast(origin = self.world_position + (0, -self.scale_y / 2, sign(z_movement) * self.scale_z / 2), terrain = self.terrain, direction = (0, 1, 0))
                        if height_ray.hit:
                            self.y += height_ray.distance / 5

        camera.rotation_x -= mouse.velocity[1] * self.sensitivity * 30 * time.dt
        self.rotation_y += mouse.velocity[0] * self.sensitivity * 30 * time.dt
        camera.rotation_x = min(max(-80, camera.rotation_x), 80)

    def input(self, key):
        if key == "space":
            if self.jump_count < 1:
                self.jump()