from ursina import *

class Arrow(Entity):
    def __init__(self):
        super().__init__(
            tag = "arrow"
        )

        self.body = Entity(model = "body", parent = self, color = "#BA8C63")
        self.tip = Entity(model = "tip", parent = self, color = color.gray)
        self.feather = Entity(model = "feather", parent = self, color = "#CC0A00")
