from ursina import *
from ursina import curve

from player import Player
from weapons.sword import Sword
from weapons.bow import Bow
from orc import Orc

from trail_renderer import TrailRenderer
from springs import Spring

app = Ursina()

# weathertop = Entity(model = "weathertop", texture = "weathertop", collider = "mesh")
# weatherhill = Entity(model = "weatherhill", texture = "weatherhill", collider = "mesh")

ground = Entity(model = "cube", color = "#CACACA", texture = "white_cube", collider = "box", scale = (100, 1, 100))

s = Sky()

light = PointLight(parent = camera, position = (0, 10, -1.5))
light.color = color.white

AmbientLight(color = color.rgba(100, 100, 100, 0.1))

sword = Sword()
sword.enabled = True

bow = Bow()
arrow = Entity(model = "arrow.obj")

player = Player("cube", (-10, 68, -7), "box", controls = "wasd")
player.jump_height = 0.3
player.SPEED = 2

player.sword = sword
player.bow = bow
player.arrow = arrow

# player.position = (57.853363037109375, -53.36747741699219, -127.7434310913086)

health_text = Text(text = str(player.health), size = 0.05, x = -0.78, y = 0.48)

def spawn_orc_1():
    orc = Orc()
    orc.follow = player
    orc.position = (6.29217, 68.3385, 2.70637)

    if player.kills != 10:
        invoke(spawn_orc_1, delay = 3)

# spawn_orc_1()

bow.parent = camera
bow.position = (0.5, 0, 1)
bow.enabled = False

trail_renderer = TrailRenderer(target = sword)
trail_renderer.disable()

def destroy_arrow():
    destroy(player.arrow)

def input(key):
    if bow.enabled and key == "right mouse down":
        player.arrow = duplicate(arrow, world_parent = bow, position = Vec3(-0.2, 0, 0), rotation = Vec3(0, 0, 0))
        player.arrow.animate("position", player.arrow.position + Vec3(0, 0, -1.2), duration = 0.2, curve = curve.linear)
        player.SPEED = 1

    elif bow.enabled and key == "right mouse up":
        player.SPEED = 2

        if mouse.hovered_entity and mouse.hovered_entity.visible:
            player.arrow.world_parent = scene
            player.arrow.animate("position", Vec3(* mouse.world_point), mouse.collision.distance / 500, curve = curve.linear, interrupt = "kill")
        
        else:
            player.arrow.world_parent = scene
            player.arrow.animate("position", player.arrow.world_position + (player.arrow.forward * 100), 0.5, curve = curve.linear, interrupt = "kill")
            destroy(player.arrow, delay = 1)

        ray = raycast(player.arrow.position, player.arrow.forward, distance = 100, ignore = [player.arrow, ])

        if ray.entity and ray.entity == sword:
            ray.entity.health -= 2
            destroy(player.arrow)

            destroy(player.arrow, delay = 10)

    if sword.enabled == True:
        if key == "left mouse down" and key != "right mouse down" and key != "right mouse up":
            sword.animate("rotation", sword.rotation + Vec3(0, 0, -90), duration = 0.05, curve = curve.linear)

            ray = raycast(player.position, player.forward, distance = 20, ignore = [sword, player, ])

            if ray.entity and ray.entity == sword:
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

    if held_keys["1"]:
        bow.disable()
        arrow.disable()
        player.arrow.disable()
        sword.enabled = True

    if held_keys["2"]:
        bow.enable()
        arrow.enable()
        sword.enabled = False

    s.rotation_y += 1 * time.dt

    if sword.enabled == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y,mouse.x, 0))
        sword.position = (movement.y * 2, movement.x * 2, movement.z * 2) + (2, 0, 2.5)

    if bow.enabled == True:
        movement = spring.update(time.dt)
        spring.shove(Vec3(mouse.y, mouse.x, 0))
        bow.position = (movement.y * 0.5, movement.x * 0.5, movement.z * 0.5) + (0.5, 0, 1)

    # print(player.position)

app.run()