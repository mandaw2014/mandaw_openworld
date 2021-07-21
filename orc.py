from ursina import *

class Orc(Entity):
    def __init__(self, position = (16, 100, 14)):
        super().__init__(
            model = "cube", 
            color = color.gray, 
            texture = "white_cube", 
            scale = (1, 3, 1), 
            collider = "box", 
            position = position,
            tag = "orc"
        )

        self.follow = None
        self.health = 5
        self.gravity = 9.81
        self.speed = 2

    def update(self):
        ray = raycast(self.position, self.down, distance = 2, ignore = [self, ])

        if self.follow.enabled == True:
            self.x += (self.follow.x - self.x) * self.speed * time.dt
            self.z += (self.follow.z - self.z) * self.speed * time.dt

            if self.health <= 0:
                self.disable()
                self.follow.kills += 1

            if not ray.hit:
                self.y -= 0.3 * self.gravity * time.dt
            
            if ray.hit and self.follow.y + 2 >= self.y:
                self.y += (self.follow.y - self.y) * self.speed * time.dt

            if ray.entity == self.follow and self.follow.blocking == False:
                self.follow.health -= 1
                self.x -= (self.follow.x - self.x) * 500 * time.dt
                self.z -= (self.follow.z - self.z) * 500 * time.dt
                self.y += 5
            if ray.entity == self.follow and self.follow.blocking == True:
                self.x -= (self.follow.x - self.x) * 1000 * time.dt
                self.z -= (self.follow.z - self.z) * 1000 * time.dt
                self.y += 5