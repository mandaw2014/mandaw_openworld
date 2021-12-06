from ursina import *

class House(Entity):
    def __init__(self, position = (0, 0, 0), rotation = (0, 0, 0)):
        super().__init__(
            model = "house",
            texture = "house",
            collider = "mesh",
            position = position,
            rotation = rotation,
            scale = (2, 2, 2),
            tag = "house"
        )

class Village(Entity):
    def __init__(self):
        super().__init__(tag = "village")

        self.house_1 = House((-579, 25.5, 208))
        self.house_2 = House((-527, 22.5, 190), (0, 90, 0))
        self.house_3 = House((-582, 25, 143), (0, 180, 0))
        self.house_4 = House((-517, 46, 63), (0, 180, 0))
        self.house_5 = House((-488, 32, 146), (0, 90, 0))
        self.house_6 = House((-632, 34, 193), (0, -90, 0))