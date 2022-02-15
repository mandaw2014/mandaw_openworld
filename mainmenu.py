from ursina import *

class MainMenu(Entity):
    def __init__(self, player):
        super().__init__(
            parent = camera.ui
        )

        self.main_menu = Entity(parent = self, enabled = True)
        self.player = player
        self.story = False

        def story():
            self.player.enable()
            mouse.locked = True
            self.main_menu.disable()
            self.player.position = (1638, 54, 437)
            self.player.sword.equipped = False
            self.player.bow.equipped = False
            self.player.shield.equipped = False
            self.story = True

        def explore():
            self.player.enable()
            mouse.locked = True
            self.main_menu.disable()
            self.player.position = (0, 300, 0)
            self.player.sword.equip()
            self.player.shield.equip()
            self.player.bow.equip()

        story_button = Button(text = "S t o r y", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        explore_button = Button(text = "E x p l o r e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)
        quit_button = Button(text = "Q u i t", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        quit_button.on_click = application.quit
        story_button.on_click = Func(story)
        explore_button.on_click = Func(explore)