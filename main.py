from ursina import *

from player import Player

from enemy import Enemy

from trail_renderer import TrailRenderer
from springs import Spring
from map import Map

app = Ursina()

scene.fog_density = 0.001

map = Map()

s = Sky()

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

player = Player("cube", (-1000, 100, 0), "box", map.terrain, controls = "wasd")
player.jump_height = 0.3
player.SPEED = 2
player.position = (-527, 100, 159)

player.sword.equipped = False
player.bow.equipped = False
player.shield.equipped = False

health_text = Text(text = str(player.health), size = 0.05, x = -0.78, y = 0.48)

e = Enemy((player.x + 10, player.y, player.z + 10), map.terrain)
e.follow = player

hit_entity = Entity(model = "sphere", scale = 0.1)

trail_renderer = TrailRenderer(target = player.sword)
trail_renderer.disable()

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
        
    s.rotation_y += 1 * time.dt

    if player.sword.enabled == True and player.sword.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y,mouse.x, 0))
        player.sword.position = (movement.y * 2, movement.x * 2, movement.z * 2) + (1.5, -2.2, 1.8)

    if player.bow.enabled == True and player.bow.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        player.bow.position = (movement.y * 0.5, movement.x * 0.5, movement.z * 0.5) + (0.5, 0, 1)

    if player.shield.enabled == True and player.shield.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        player.shield.position = (movement.y * 0.2, movement.x * 0.2, movement.z * 0.2) + (-1, -1, 1)

app.run()
