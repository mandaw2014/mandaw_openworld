from ursina import *

class Shield(FrameAnimation3d):
    def __init__(self, rotation = (0, 90, 90), position = (-522, 18.5, 191), terrain = None):
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
        self.strokes = 0
        self.player = None
        self.sword = None
        self.arrow = None
        self.grappling_hook = None
        self.bow = None

        self.always_on_top = False

        self.blocking = False
        self.gravity = False

        self.terrain = terrain

        self.pause()

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.parent = camera
            self.position = (-1, -1, 1)
            self.rotation = (0, 90, 0)
            self.gravity = False
            self.bow.equipped = False
            self.bow.parent = scene
            
            if self.bow.equipped == True:
                self.bow.disable()
                self.arrow.disable()
        
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
        if self.enabled == True and self.equipped == True:
            if key == "right mouse down":
                if self.strokes <= 2:
                    self.resume()

                self.strokes += 1

                if self.strokes == 2:
                    invoke(self.reset_shield, delay = 0.33)

                if self.strokes < 2:
                    invoke(self.pause, delay = 0.33) 

    def reset_shield(self):
        self.finish()
        self.start()
        self.pause()
        self.strokes = 0

    def equip(self):
        self.equipped = True
        self.parent = camera
        self.position = (-1, -1, 1)
        self.rotation = (0, 90, 0)
        self.gravity = False
        
        if self.bow.equipped == True:
            self.bow.disable()
            self.arrow.disable()