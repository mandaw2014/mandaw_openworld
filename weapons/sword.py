from ursina import *
from ursina.shaders import ssao_shader

class Sword(Entity):
    def __init__(self, position = (2, 0, 2.5), rotation = (0, 90, 0), parent = camera):
        super().__init__(
            model = "sword.obj",
            parent = parent,
            position = position,
            rotation = rotation,
            shader = ssao_shader,
            tag = "sword",
            texture = "sword.png"
        )