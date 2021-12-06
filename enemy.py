from ursina import *

class Enemy(Entity):
    def __init__(self, position = (16, 5, 14), terrain = None):
        super().__init__(
            model = "cube", 
            color = color.gray, 
            texture = "white_cube", 
            scale = (1, 3, 1), 
            collider = "box", 
            position = position,
            tag = "enemy"
        )

        self.follow = None
        self.health = 3
        self.gravity = 9.81
        self.speed = 2

        self.terrain = terrain

    def update(self):
        ray = terraincast(origin = self.position, direction = self.down, terrain = self.terrain, distance = 2)
        
        if self.follow.enabled == True:
            self.x += (self.follow.x - self.x) * self.speed * time.dt
            self.z += (self.follow.z - self.z) * self.speed * time.dt

            if self.health <= 0:
                self.disable()
                self.follow.kills += 1

            if not ray.hit:
                self.y -= 1 * self.gravity * time.dt
            
            if ray.hit and self.follow.y + 2 >= self.y:
                self.y += (self.follow.y - self.y) * self.speed * time.dt

            hit_ray = raycast(origin = self.position, direction = self.forward, distance = 4, ignore = [self.follow, ])

            if hit_ray.entity and hit_ray.entity.tag == "player":
                self.hit()

    def input(self, key):
        hit = raycast(origin = self.follow.position, direction = self.follow.forward, distance = 10, ignore = [self.follow, ])

        if key == "left mouse down" and hit.entity == self and self.follow.sword.equipped == True:
            invoke(self.hit, delay = 0.5)

    def hit(self):
        self.health -= 1
        self.x -= (self.follow.x - self.x) * 100 * time.dt
        self.z -= (self.follow.z - self.z) * 100 * time.dt
