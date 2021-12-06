from ursina import *
from ursina import curve

class Bow(Entity):
    def __init__(self, model = "bow.obj", loaded = False, terrain = None):
        super().__init__(
            model = model,
            texture = "bow",
            tag = "bow",
            parent = scene,
            position = (-588, 21, 144),
            rotation = (0, 90, 90)
        )

        self.loaded = loaded
        self.equipped = False
        self.player = None
        self.sword = None
        self.arrow = None
        self.shield = None
        self.grappling_hook = None
        self.gravity = False

        self.terrain = terrain

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.gravity = False
            self.parent = camera
            self.position = (0.5, 0, 1)
            self.rotation = (0, 0, 0)
            self.shield.equipped = False
            self.shield.parent = scene

            if self.sword.equipped == True:
                self.sword.disable()
                self.arrow.enable() 
            if self.shield.equipped == True:
                self.shield.disable()
        
        if held_keys["q"] and self.equipped == True:
            self.equipped = False
            self.gravity = True
            self.parent = scene
            self.position = self.player.position
            self.y = self.player.y + 1

        ray = terraincast(origin = self.position, direction = self.down, terrain = self.terrain, distance = 1.5)

        if self.equipped == False and self.gravity == True and not ray.hit:
            self.y -= 1 * 9.81 * time.dt 

    def input(self, key):
        if self.enabled and key == "right mouse down" and self.equipped == True:
            self.player.arrow = duplicate(self.arrow, world_parent = self, position = Vec3(-0.2, 0, 0), rotation = Vec3(0, 0, 0))
            self.player.arrow.animate("position", self.player.arrow.position + Vec3(0, 0, -1.2), duration = 0.2, curve = curve.linear)
            self.player.SPEED = 1

        elif self.enabled and key == "right mouse up" and self.equipped == True:
            self.player.SPEED = 2

            if mouse.hovered_entity and mouse.hovered_entity.visible:
                self.player.arrow.world_parent = scene
                self.player.arrow.animate("position", Vec3(* mouse.world_point), mouse.collision.distance / 10000, curve = curve.linear, interrupt = "kill")
            
            else:
                self.player.arrow.world_parent = scene
                self.player.arrow.animate("position", self.player.arrow.world_position + (self.player.arrow.forward * 100), 0.5, curve = curve.linear, interrupt = "kill")
                destroy(self.player.arrow, delay = 1)

            ray = raycast(origin = self.player.arrow.position, direction = self.player.arrow.forward, distance = 100, ignore = [self.player, self, self.arrow, ])

            if ray.entity and ray.entity.tag == "enemy":
                ray.entity.hit()
                destroy(self.player.arrow, delay = 0.07)
            
            destroy(self.player.arrow, delay = 1)