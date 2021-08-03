from ursina import *

from player import Player

from weapons.sword import Sword
from weapons.bow import Bow
from weapons.arrow import Arrow 
from weapons.shield import Shield
from weapons.grappling_hook import *

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

# village_1 = Village()

s = Sky()

light = PointLight(parent = camera, position = (0, 10, -1.5))
light.color = color.white

AmbientLight(color = color.rgba(100, 100, 100, 0.1))

sword = Sword()
bow = Bow()
arrow = Arrow()
shield = Shield()
grappling_hook = GrapplingHook()

player = Player("cube", (-1000, 100, 0), "box", controls = "wasd")
player.jump_height = 0.3
player.SPEED = 2
# player.position = (-527, 255, 159)
player.sword = sword
player.bow = bow
player.arrow = arrow

sword.player = player
sword.bow = bow
sword.arrow = arrow
sword.shield = shield
sword.grappling_hook = grappling_hook

bow.player = player
bow.sword = sword
bow.arrow = arrow
bow.shield = shield
bow.grappling_hook = grappling_hook

shield.player = player
shield.bow = bow
shield.sword = sword
shield.arrow = arrow
shield.grappling_hook = grappling_hook

grappling_hook.player = player
grappling_hook.sword = sword
grappling_hook.arrow = arrow
grappling_hook.shield = shield
grappling_hook.bow = bow

grapple_1 = GrappleBlock((-963, 52, 60))
grapple_2 = GrappleBlock((-973, 72, 70))
grapple_3 = GrappleBlock((-963, 92, 60))

grapple_1.grappling_hook = grappling_hook
grapple_1.player = player
grapple_2.grappling_hook = grappling_hook
grapple_2.player = player
grapple_3.grappling_hook = grappling_hook
grapple_3.player = player

health_text = Text(text = str(player.health), size = 0.05, x = -0.78, y = 0.48)

def spawn_orc_1():
    orc = Orc()
    orc.follow = player
    orc.position = (6.29217, 68.3385, 2.70637)

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

    if held_keys["1"] and sword.equipped == True and bow.equipped == True and grappling_hook.equipped == True:
        bow.disable()
        arrow.disable()
        player.arrow.disable()
        grappling_hook.enabled = False
        sword.enabled = True

    if held_keys["2"] and sword.equipped == True and bow.equipped == True and grappling_hook.equipped == True:
        bow.enable()
        arrow.enable()
        grappling_hook.enabled = False
        sword.enabled = False

    if held_keys["3"] and sword.equipped == True and bow.equipped == True and grappling_hook.equipped == True:
        bow.disable()
        arrow.disable()
        grappling_hook.enabled = True
        sword.enabled = False

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

    if grappling_hook.enabled == True and grappling_hook.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        grappling_hook.position = (movement.y * 2, movement.x * 2, movement.z * 2) + (1, -1, 2)

    print(round(player.position))

app.run()
