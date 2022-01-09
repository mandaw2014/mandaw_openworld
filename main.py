from ursina import *

from player import Player

from enemy import Enemy

from springs import Spring
from map import Map

app = Ursina()

scene.fog_density = 0.001

map = Map()

Sky(texture = "sky")

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

player = Player((1638, 54, 437), map)
player.jump_height = 0.3
player.position = (1980, 200, 96)

player.sword.equipped = False
player.bow.equipped = False
player.shield.equipped = False

player.sword.enable()
player.sword.position = (2012, 130, 97)

health_text = Text(text = str(player.health), size = 0.05, x = -0.78, y = 0.48)

hit_entity = Entity(model = "sphere", scale = 0.1)

spring = Spring()

enemy_1 = Enemy((0, 0, 0), map.terrain)
enemy_1.follow = player
enemy_1.disable()

enemy_2 = Enemy((0, 0, 0), map.terrain)
enemy_2.follow = player
enemy_2.disable()

enemy_3 = Enemy((0, 0, 0), map.terrain)
enemy_3.follow = player
enemy_3.disable()

enemy_1.position = (1980, 140, 96)
enemy_2.position = (1996, 140, 122)
enemy_3.position = (1988, 140, 112)

debug = False

def update():
    if held_keys["escape"]:
        mouse.locked = False
    if held_keys["left mouse"]:
        mouse.locked = True
    if held_keys["g"]:
        player.position = (1638, 54, 437)
    if player.y <= -50:
        player.y = player.y + 500

    global debug

    if held_keys["right shift"]:
        debug = not debug

    if held_keys["p"]:
        print(player.position)

    if debug == True:
        player.disable()
        player.sword.disable(); player.bow.disable(); player.shield.disable()
        EditorCamera()

    health_text.text = str(player.health)

    if held_keys["1"] and player.sword.equipped == True and player.bow.equipped == True:
        if player.shield.equipped == True:
            player.shield.enable()

        player.bow.disable()
        player.arrow.disable()
        player.sword.enable()

    if held_keys["2"] and player.sword.equipped == True and player.bow.equipped == True:
        if player.shield.equipped == True and player.shield.enabled == True:
            player.shield.disable()
            
        player.bow.enable()
        player.arrow.enable()
        player.sword.disable()

    if player.sword.enabled == True and player.sword.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y,mouse.x, 0))
        player.sword.position = (movement.y * 2, movement.x * 2, movement.z * 2) + (1.5, -2.2, 1.8)

    if player.bow.enabled == True and player.bow.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        if player.bow.loaded == False:
            player.bow.position = (movement.y * 0.5, movement.x * 0.5, movement.z * 0.5) + (0.5, 0, 1)
        elif player.bow.loaded == True:
            player.bow.position = (movement.y * 0.1, movement.x * 0.1, movement.z * 0.1) + (0.5, 0, 1)

    if player.shield.enabled == True and player.shield.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        player.shield.position = (movement.y * 0.2, movement.x * 0.2, movement.z * 0.2) + (-1, -1, 1)

    ###############################
    # STORY
    ###############################

    if player.sword.equipped == True:
        enemy_1.enable()
        enemy_2.enable()
        enemy_3.enable()

app.run()