from ursina import *

class House(Entity):
    def __init__(self, position = (0, 0, 0), rotation = (0, 0, 0)):
        super().__init__(
            model = "house.obj",
            texture = "house.png",
            collider = "mesh",
            position = position,
            rotation = rotation,
            scale = (13, 13, 13),
            tag = "house"
        )

class Village(Entity):
    def __init__(self):
        super().__init__(tag = "village")

        self.house_1 = House((-579.738, 24, 208.46))