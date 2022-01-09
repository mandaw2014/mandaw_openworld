from ursina import *
from village import Village

class Map(object):
    def __init__(self):
        # Map
        self.terrain = Entity(model = Terrain("heightmap", skip = 8), texture = "colour", scale = 2000, scale_y = 1000, collider = "mesh", tag = "terrain")

        self.sorntop_minonka = Entity(model = "sorntop", texture = "sorntop", collider = "mesh", tag = "sorntop", position = (2000, 60, 100), rotation = (0, 90, 0))
        self.sornhill_minonka = Entity(model = "sornhill", texture = "sornhill", collider = "mesh", tag = "sornhill", position = (2000, 60, 100), rotation = (0, 90, 0))

        self.sorntop_rockshell = Entity(model = "sorntop", texture = "sorntop", collider = "mesh", tag = "sorntop", position = (300, 100, -850))
        self.sornhill_rockshell = Entity(model = "sornhill", texture = "sornhill", collider = "mesh", tag = "sornhill", position = (300, 100, -850))

        self.sorntop_mandaw = Entity(model = "sorntop", texture = "sorntop", collider = "mesh", tag = "sorntop", position = (1200, 100, -700), scale = (0.7, 0.7, 0.7))
        self.sornhill_mandaw = Entity(model = "sornhill", texture = "sornhill", collider = "mesh", tag = "sornhill", position = (1200, 100, -700), scale = (0.7, 0.7, 0.7))