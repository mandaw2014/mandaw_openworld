from ursina import *

class Sword(FrameAnimation3d):
    def __init__(self, rotation = (90, 90, 0), parent = scene):
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

        self.pause()

    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.gravity = False
            self.parent = camera
            self.position = (1.5, -2.2, 1.8)
            self.rotation = (0, 90, 0)

            if self.bow.equipped == True:
                self.bow.disable()
                self.arrow.disable()
            if self.shield.equipped == True:
                self.always_on_top = False
                self.shield.always_on_top = True
        
        if held_keys["q"] and self.equipped == True:
            self.equipped = False
            self.gravity = True
            self.parent = scene
            self.position = self.player.position
            self.y = self.player.y + 1

        ray = raycast(self.position, self.down, distance = 1, ignore = [self, self.player, ])

        if self.equipped == False and self.gravity == True and not ray.hit:
            self.y -= 1 * 9.81 * time.dt 

        if self.equipped == True and self.shield.equipped == False:
            self.always_on_top = True
        else:
            self.always_on_top = False

    def input(self, key):
        if self.enabled == True and self.equipped == True:
            if key == "left mouse down":
                if self.strokes <= 2:
                    self.resume()

                self.strokes += 1

                if self.strokes == 2:
                    invoke(self.reset_sword, delay = 1.392)

                if self.strokes < 2:
                    invoke(self.pause, delay = 1.392) 

    def reset_sword(self):
        self.finish()
        self.start()
        self.pause()
        self.strokes = 0

    # if self.enabled == True and self.parent == camera and self.equipped == True:
    #     if key == "left mouse down" and key != "right mouse down" and key != "right mouse up":
    #         self.animate("position", self.position + Vec3(0, 1, -2), duration = 0.05, curve = curve.linear)
    #         self.animate("rotation", self.rotation + Vec3(0, 0, 60), duration = 0.05, curve = curve.linear)

    #         ray = raycast(self.player.position, self.player.forward, distance = 20, ignore = [self, self.player, ])

    #         if ray.entity and ray.entity.tag == "orc":
    #             ray.entity.health -= 1

    #     elif key == "left mouse up" and key != "right mouse down" and key != "right mouse up":
    #         invoke(self.reset_sword, delay = 0.3) 

    #     if key == "right mouse down" and key != "left mouse down" and key != "left mouse up" :
    #         self.animate("rotation", self.rotation + Vec3(-65, 0, 0), duration = 0.05, curve = curve.linear)
    #         self.player.SPEED = 0.5
    #         self.player.blocking = True

    #     elif key == "right mouse up" and key != "left mouse down" and key != "left mouse up":
    #         self.animate("rotation", self.rotation + Vec3(-self.rotation_x, 0, 0), duration = 0.05, curve = curve.linear)
    #         self.player.SPEED = 2
    #         self.player.blocking = False