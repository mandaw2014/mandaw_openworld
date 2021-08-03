from ursina import *

class Shield(FrameAnimation3d):
    def __init__(self, rotation = (0, 90, 0), position = (-953, 52, 45)):
        super().__init__(
            name = "shield_",
            autoplay = False,
            loop = True,
            fps = 60,
            frame_times = 20,
            texture = "shield",
            collider = "mesh",
            parent = scene,
            tag = "shield",
            position = position,
            rotation = rotation
        )

        self.equipped = False
        self.player = None
        self.sword = None
        self.arrow = None
        self.grappling_hook = None
        self.bow = None

        self.blocking = False

        self.pause()

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.parent = camera
            self.position = (-1, -1, 1)
            
            if self.bow.equipped == True:
                self.bow.disable()
                self.arrow.disable()
            if self.grappling_hook.equipped == True:
                self.grappling_hook.disable()
        
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

        if self.blocking == False:
            self.player.SPEED = 2

    def input(self, key):
        if self.enabled == True and self.equipped == True:
            if key == "right mouse down":
                self.resume()
                self.player.SPEED = 0.5
                self.blocking = not self.blocking
                invoke(self.reset_shield, delay = 0.33)

    def reset_shield(self):
        self.pause()