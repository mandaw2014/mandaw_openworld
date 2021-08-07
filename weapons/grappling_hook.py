from ursina import *
from ursina import curve

class GrapplingHook(Entity):
    def __init__(self, position = (-963, 32, 60)):
        super().__init__(
            model = "cube",
            parent = scene,
            color = color.dark_gray,
            texture = "white_cube",
            collider = "box",
            position = position,
            tag = "grappling_hook",
        )

        self.equipped = False
        self.player = None
        self.sword = None
        self.arrow = None
        self.bow = None
        self.shield = None
        
    def update(self):
        if held_keys["e"] and distance(self.player, self) <= 10:
            self.equipped = True
            self.parent = camera
            self.position = (1, -1, 2)

            if self.sword.equipped == True:
                self.sword.disable()
                self.arrow.enable()
            if self.bow.equipped == True:
                self.bow.disable()
                self.arrow.disable()
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

class GrappleBlock(Button):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(
            parent = scene,
            model = "cube",
            color = color.red,
            texture = "white_cube",
            collider = "box",
            position = position,
            tag = "grapple_block"
        )

        self.player = None
        self.grappling_hook = None

    def update(self):
        if self.grappling_hook.equipped == True and self.grappling_hook.enabled == True:
            self.on_click = Func(self.player.animate_position, self.position, duration = 0.5, curve = curve.linear)

            ray = raycast(self.player.position, self.player.forward, distance = 1, ignore = [self.player, ])

            if ray.entity == self:
                self.player.y += 2