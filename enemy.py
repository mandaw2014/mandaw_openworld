from ursina import *

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

class Enemy(Entity):
    def __init__(self, position = (16, 5, 14), terrain = None):
        super().__init__(
            model = "cube", 
            color = color.gray, 
            texture = "white_cube", 
            scale = (1, 2.5, 1), 
            collider = "box", 
            position = position,
            tag = "enemy"
        )

        self.follow = None
        self.health = 3
        self.gravity = 9.81
        self.speed = 1

        self.velocity_y = 0

        self.terrain = terrain

    def update(self):
        y_movement = self.velocity_y * time.dt

        self.direction = Vec3(self.forward + self.right)

        self.direction = (0, sign(y_movement), 0)
        y_ray = terraincast(origin = self.world_position, direction = self.direction, terrain = self.terrain, distance = self.scale_y + abs(y_movement))

        if y_ray.hit:
            self.velocity_y = 0
        else:
            self.y += y_movement
            self.velocity_y -= 5 * time.dt

        if self.y <= -100:
            self.y = self.follow.y + 10
        
        x_movement = ((self.follow.x - self.x) * self.speed * time.dt)
        z_movement = ((self.follow.z - self.z) * self.speed * time.dt)
        
        if self.follow.enabled == True:
            if x_movement != 0:
                self.direction = (sign(x_movement), 0, 0)
                x_ray = terraincast(origin = self.world_position, terrain = self.terrain, direction = self.direction, distance = self.scale_x + abs(x_movement))

                if not x_ray.hit:
                    self.x += x_movement
                else:
                    top_x_ray = terraincast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), terrain = self.terrain, direction = self.direction, distance = self.scale_x + math.tan(math.radians(100000000)))

                    if not top_x_ray.hit:
                        self.x += x_movement
                        height_ray = terraincast(origin = self.world_position + (sign(x_movement) * self.scale_x / 2, -self.scale_y / 2, 0), terrain = self.terrain, direction = (0, 1, 0))
                        if height_ray.hit:
                            self.y += height_ray.distance / 5

            if z_movement != 0:
                self.direction = (0, 0, sign(z_movement))
                z_ray = terraincast(origin = self.world_position, terrain = self.terrain, direction = self.direction, distance = self.scale_z + abs(z_movement))

                if not z_ray.hit:
                    self.z += z_movement
                else:
                    top_z_ray = terraincast(origin = self.world_position - (0, self.scale_y / 2 -0.1, 0), terrain = self.terrain, direction = self.direction, distance = self.scale_z + math.tan(math.radians(100000000)))

                    if not top_z_ray.hit:
                        self.z += z_movement
                        height_ray = terraincast(origin = self.world_position + (0, -self.scale_y / 2, sign(z_movement) * self.scale_z / 2), terrain = self.terrain, direction = (0, 1, 0))
                        if height_ray.hit:
                            self.y += height_ray.distance / 5

            if self.health <= 0:
                self.disable()
            
            hit_ray = boxcast(origin = self.position, direction = self.forward, distance = 6, ignore = [self, ])

            if hit_ray.entity == self.follow:
                self.pushed()
                if not self.follow.shield.equipped and not self.follow.shield.blocking:
                    self.follow.health -= 1

    def input(self, key):
        hit = boxcast(origin = self.follow.position, direction = self.follow.forward, distance = 15, ignore = [self.follow, ])

        if key == "left mouse down" and hit.entity == self and self.follow.sword.equipped == True:
            invoke(self.hit, delay = 0.6)

    def hit(self):
        self.health -= 1
        self.x -= (self.follow.x - self.x) * 100 * time.dt
        self.z -= (self.follow.z - self.z) * 100 * time.dt

    def pushed(self):
        self.x -= (self.follow.x - self.x) * 150 * time.dt
        self.z -= (self.follow.z - self.z) * 150 * time.dt