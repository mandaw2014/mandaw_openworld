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

player = Player((-1000, 100, 0), map.terrain)
player.jump_height = 0.3
player.SPEED = 2
player.position = (-527, 100, 159)

player.sword.equipped = False
player.bow.equipped = False
player.shield.equipped = False

health_text = Text(text = str(player.health), size = 0.05, x = -0.78, y = 0.48)

enemy = Enemy((player.x + 50, 50, player.z + 50), map.terrain)
enemy.follow = player

hit_entity = Entity(model = "sphere", scale = 0.1)

spring = Spring()

def update():
    if held_keys["escape"]:
        mouse.locked = False
    if held_keys["left mouse"]:
        mouse.locked = True
    if held_keys["g"]:
        player.position = (16, 100, 14)
    if player.y <= -100:
        player.position = (16, 100, 14)

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

app.run()
