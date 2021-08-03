from ursina import *
from ursina import curve

class Bow(Entity):
    def __init__(self, model = "bow.obj", loaded = False):
        super().__init__(
            model = model,
            texture = "bow",
            tag = "bow",
            parent = scene,
            position = (-963, 32, 50)
        )

        self.loaded = loaded
        self.equipped = False
        self.player = None
        self.sword = None
        self.arrow = None
        self.shield = None
        self.grappling_hook = None

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.parent = camera
            self.position = (0.5, 0, 1)

            if self.sword.equipped == True:
                self.sword.disable()
                self.arrow.enable() 
            if self.grappling_hook.equipped == True:
                self.grappling_hook.disable()
            if self.shield.equipped == True:
                self.shield.disable()
        
        if held_keys["q"] and self.equipped == True:
            self.equipped = False
            self.parent = scene
            self.position = self.player.position
            self.y = self.player.y + 1

        ray = raycast(self.position, self.down, distance = 1.5, ignore = [self, self.player, ])

        if self.equipped == False and not ray.hit:
            self.y -= 1 * 9.81 * time.dt 

        if self.equipped == True:
            self.always_on_top = True
        else:
            self.always_on_top = False

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

            ray = raycast(self.player.arrow.position, self.player.arrow.forward, distance = 100, ignore = [self.player.arrow, self.player, ])

            if ray.entity and ray.entity.tag == "orc":
                ray.entity.health -= 2
                destroy(self.player.arrow, delay = 0.07)
            
            destroy(self.player.arrow, delay = 1)
