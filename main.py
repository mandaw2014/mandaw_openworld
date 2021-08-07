from ursina import *

from player import Player

from weapons.sword import Sword
from weapons.bow import Bow
from weapons.arrow import Arrow 
from weapons.shield import Shield

from orc import Orc

from trail_renderer import TrailRenderer
from springs import Spring

from village import Village

app = Ursina()

scene.fog_density = 0.001

# Map
terrain = Entity(model = Terrain("heightmap", skip = 8), texture = "colour", scale = 2000, scale_y = 1000, collider = "mesh", tag = "terrain")

sorntop_minonka = Entity(model = "sorntop", texture = "sorntop", collider = "mesh", tag = "sorntop", position = (2000, 60, 100))
sornhill_minonka = Entity(model = "sornhill", texture = "sornhill", collider = "mesh", tag = "sornhill", position = (2000, 60, 100))

sorntop_rockshell = Entity(model = "sorntop", texture = "sorntop", collider = "mesh", tag = "sorntop", position = (300, 100, -850))
sornhill_rockshell = Entity(model = "sornhill", texture = "sornhill", collider = "mesh", tag = "sornhill", position = (300, 100, -850))

sorntop_mandaw = Entity(model = "sorntop", texture = "sorntop", collider = "mesh", tag = "sorntop", position = (1200, 100, -700), scale = (0.7, 0.7, 0.7))
sornhill_mandaw = Entity(model = "sornhill", texture = "sornhill", collider = "mesh", tag = "sornhill", position = (1200, 100, -700), scale = (0.7, 0.7, 0.7))

village_1 = Village()

s = Sky()

light = PointLight(parent = camera, position = (0, 10, -1.5))
light.color = color.white

AmbientLight(color = color.rgba(100, 100, 100, 0.1))

sword = Sword()
bow = Bow()
arrow = Arrow()
shield = Shield()

player = Player("cube", (-1000, 100, 0), "box", controls = "wasd")
player.jump_height = 0.3
player.SPEED = 2
player.position = (-527, 100, 159)
player.sword = sword
player.bow = bow
player.arrow = arrow

sword.player = player
sword.bow = bow
sword.arrow = arrow
sword.shield = shield

bow.player = player
bow.sword = sword
bow.arrow = arrow
bow.shield = shield

shield.player = player
shield.bow = bow
shield.sword = sword
shield.arrow = arrow

health_text = Text(text = str(player.health), size = 0.05, x = -0.78, y = 0.48)

def spawn_orc_1():
    orc = Orc()
    orc.follow = player
    orc.position = (-547, 100, 179)

# spawn_orc_1()

# player.disable()
# EditorCamera() 
# sword.disable()

trail_renderer = TrailRenderer(target = sword)
trail_renderer.disable()

def destroy_arrow():
    destroy(player.arrow)

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

    if held_keys["1"] and sword.equipped == True and bow.equipped == True:
        if shield.equipped == True:
            shield.enable()

        bow.disable()
        arrow.disable()
        player.arrow.disable()
        sword.enable()

    if held_keys["2"] and sword.equipped == True and bow.equipped == True:
        if shield.equipped == True and shield.enabled == True:
            shield.disable()
            
        bow.enable()
        arrow.enable()
        sword.disable()
        
    s.rotation_y += 1 * time.dt

    if sword.enabled == True and sword.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y,mouse.x, 0))
        sword.position = (movement.y * 2, movement.x * 2, movement.z * 2) + (1.5, -2.2, 1.8)

    if bow.enabled == True and bow.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        bow.position = (movement.y * 0.5, movement.x * 0.5, movement.z * 0.5) + (0.5, 0, 1)

    if shield.enabled == True and shield.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        shield.position = (movement.y * 0.2, movement.x * 0.2, movement.z * 0.2) + (-1, -1, 1)

    print(round(player.position, 0))

app.run()
