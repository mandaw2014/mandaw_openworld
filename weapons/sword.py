from ursina import *
from terraincast import terraincast

class Sword(FrameAnimation3d):
    def __init__(self, rotation = (0, 0, 0), parent = scene, terrain = None):
        super().__init__(
            "sword_",
            frame_times = 140,
            fps = 100,
            parent = parent,
            position = (-579, 21.35, 213.5),
            # position = (1.5, -2.2, 1.8),
            rotation = rotation,
            scale = (4, 4, 4),
            tag = "sword",
            texture = "sword.png",
            autoplay = False,
        )

        self.equipped = False
        self.strokes = 0
        self.player = None
        self.bow = None
        self.arrow = None
        self.shield = None
        self.grappling_hook = None
        self.gravity = False

        self.always_on_top = False

        self.ready = True

        self.terrain = terrain

        self.pause()

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.gravity = False
            self.parent = camera
            self.position = (1.5, -2.2, 1.8)
            self.rotation = (0, 90, 0)
            if self.bow.equipped == True:
                self.bow.equipped = False
                self.bow.parent = scene
        
        if held_keys["q"] and self.equipped == True:
            self.equipped = False
            self.gravity = True
            self.parent = scene
            self.position = self.player.position
            self.y = self.player.y + 1

        ray = terraincast(origin = self.position, direction = self.down, terrain = self.terrain, distance = 1)

        if self.equipped == False and self.gravity == True and not ray.hit:
            self.y -= 1 * 9.81 * time.dt 

    def input(self, key):
        if self.enabled == True and self.equipped == True:
            if key == "left mouse down":
                if self.ready == True:
                    if self.strokes <= 2:
                        self.resume()

                    self.strokes += 1

                    if self.strokes == 2:
                        self.ready = False
                        invoke(self.reset_sword, delay = 1.392)

                    if self.strokes < 2:
                        self.ready = False
                        invoke(self.pause_sword, delay = 1.392) 

    def reset_sword(self):
        self.ready = True
        self.finish()
        self.start()
        self.pause()
        self.strokes = 0

    def pause_sword(self):
        self.ready = True
        self.pause()

    def equip(self):
        self.equipped = True
        self.gravity = False
        self.parent = camera
        self.position = (1.5, -2.2, 1.8)
        self.rotation = (0, 90, 0)

        if self.bow.equipped == True:
            self.bow.disable()