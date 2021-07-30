from ursina import *

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

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.parent = camera
            self.position = (0.5, 0, 1)

            if self.sword.equipped == True:
                self.sword.disable()
                self.arrow.enable()
        
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
