from ursina import *
from ursina import curve

from player import Player
from weapons.sword import Sword
from weapons.bow import Bow
from weapons.arrow import Arrow 
from orc import Orc

from trail_renderer import TrailRenderer
from springs import Spring

from village import Village

app = Ursina()

# scene.fog_density = 0.001

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

bow.player = player
bow.sword = sword
bow.arrow = arrow

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

def input(key):
    if bow.enabled and key == "right mouse down" and bow.equipped == True:
        player.arrow = duplicate(arrow, world_parent = bow, position = Vec3(-0.2, 0, 0), rotation = Vec3(0, 0, 0))
        player.arrow.animate("position", player.arrow.position + Vec3(0, 0, -1.2), duration = 0.2, curve = curve.linear)
        player.SPEED = 1

    elif bow.enabled and key == "right mouse up" and bow.equipped == True:
        player.SPEED = 2

        if mouse.hovered_entity and mouse.hovered_entity.visible:
            player.arrow.world_parent = scene
            player.arrow.animate("position", Vec3(* mouse.world_point), mouse.collision.distance / 10000, curve = curve.linear, interrupt = "kill")
        
        else:
            player.arrow.world_parent = scene
            player.arrow.animate("position", player.arrow.world_position + (player.arrow.forward * 100), 0.5, curve = curve.linear, interrupt = "kill")
            destroy(player.arrow, delay = 1)

        ray = raycast(player.arrow.position, player.arrow.forward, distance = 100, ignore = [player.arrow, player, ])

        if ray.entity and ray.entity.tag == "orc":
            ray.entity.health -= 2
            destroy(player.arrow, delay = 0.07)
        
        destroy(player.arrow, delay = 1)

    if sword.enabled == True and sword.parent == camera and sword.equipped == True:
        if key == "left mouse down" and key != "right mouse down" and key != "right mouse up":
            sword.animate("rotation", sword.rotation + Vec3(0, 0, -90), duration = 0.05, curve = curve.linear)

            ray = raycast(player.position, player.forward, distance = 20, ignore = [sword, player, ])

            if ray.entity and ray.entity.tag == "orc":
                ray.entity.health -= 1

        elif key == "left mouse up" and key != "right mouse down" and key != "right mouse up":
            sword.animate("rotation", sword.rotation - (0, 0, sword.rotation_z), duration = 0.05, curve = curve.linear)

        if key == "right mouse down" and key != "left mouse down" and key != "left mouse up" :
            sword.animate("rotation", sword.rotation + Vec3(-65, 0, 0), duration = 0.05, curve = curve.linear)
            player.SPEED = 0.5
            player.blocking = True

        elif key == "right mouse up" and key != "left mouse down" and key != "left mouse up":
            sword.animate("rotation", sword.rotation + Vec3(-sword.rotation_x, 0, 0), duration = 0.05, curve = curve.linear)
            player.SPEED = 2
            player.blocking = False

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
        bow.disable()
        arrow.disable()
        player.arrow.disable()
        sword.enabled = True

    if held_keys["2"] and sword.equipped == True and bow.equipped == True:
        bow.enable()
        arrow.enable()
        sword.enabled = False

    s.rotation_y += 1 * time.dt

    if sword.enabled == True and sword.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y,mouse.x, 0))
        sword.position = (movement.y * 2, movement.x * 2, movement.z * 2) + (2, 0, 2.5)

    if bow.enabled == True and bow.equipped == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        bow.position = (movement.y * 0.5, movement.x * 0.5, movement.z * 0.5) + (0.5, 0, 1)

    print(player.position)

app.run()
