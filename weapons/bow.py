from ursina import *

class Bow(Entity):
    def __init__(self, model = "bow.obj", loaded = False):
        super().__init__(
            model = model,
            texture = "bow",
            tag = "bow"
        )

        self.loaded = loaded