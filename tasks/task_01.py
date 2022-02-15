from ursina import *

class Task1_FindSword(Entity):
    def __init__(self, player):
        super().__init__(parent = camera.ui)
        self.tasks = Entity(parent = self, enabled = True)
        self.player = player

        self.task_text = Text(text = "Sword: " + str(round(distance(self.player, self.player.sword))), origin = (0, 0), size = 0.05, position = (0, 0.4))

    def find_sword(self):
        self.task_text.text = "Sword: " + str(round(distance_xz(self.player, self.player.sword) / 10))