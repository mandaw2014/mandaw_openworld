from ursina import *

class Arrow(Entity):
    def __init__(self):
        super().__init__(
            model = "body",
            color = "#BA8C63",
            scale = (0.7, 0.7, 0.7),
            tag = "arrow"
        )

        self.tip = Entity(model = "tip", parent = self, color = color.gray),
        self.feather = Entity(model = "feather", parent = self, color = "#CC0A00")