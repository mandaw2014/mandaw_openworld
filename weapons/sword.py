from ursina import *

class Sword(Entity):
    def __init__(self, rotation = (0, 90, 0), parent = scene):
        super().__init__(
            model = "sword.obj",
            parent = parent,
            position = (-971, 50, 34),
            rotation = rotation,
            tag = "sword",
            texture = "sword.png"
        )

        self.equipped = False
        self.player = None
        self.bow = None
        self.arrow = None

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.parent = camera
            self.position = (2, 0, 2.5)

            if self.bow.equipped == True:
                self.bow.disable()
                self.arrow.disable()
        
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
