from ursina import *

class Sword(FrameAnimation3d):
    def __init__(self, rotation = (0, 90, 0), parent = scene):
        super().__init__(
            "sword_",
            frame_times = 140,
            fps = 100,
            parent = parent,
            position = (-963, 52, 35),
            rotation = rotation,
            scale = (4, 4, 4),
            tag = "sword",
            texture = "sword.png",
            autoplay = False,
        )

        self.equipped = False
        self.player = None
        self.bow = None
        self.arrow = None
        self.shield = None
        self.grappling_hook = None

        self.pause()

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.parent = camera
            self.position = (1.5, -2.2, 1.8)

            if self.bow.equipped == True:
                self.bow.disable()
                self.arrow.disable()
            if self.grappling_hook.equipped == True:
                self.grappling_hook.disable()
            if self.shield.equipped == True:
                self.always_on_top = False
                self.shield.always_on_top = True
        
        if held_keys["q"] and self.equipped == True:
            self.equipped = False
            self.parent = scene
            self.position = self.player.position
            self.y = self.player.y + 1

        ray = raycast(self.position, self.down, distance = 1.5, ignore = [self, self.player, ])

        if self.equipped == False and not ray.hit:
            self.y -= 1 * 9.81 * time.dt 

        # if self.equipped == True:
        #     self.always_on_top = True
        # if self.shield.equipped == True:
        #     self.always_on_top = False
        # elif self.equipped == False:
        #     self.always_on_top = False

    def input(self, key):
        if self.enabled == True and self.equipped == True:
            if key == "left mouse down":
                self.resume()
                self.player.SPEED = 1
                invoke(self.reset_sword, delay = 1.4)


    def reset_sword(self):
        self.pause()
        self.player.SPEED = 2
