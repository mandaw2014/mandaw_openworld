from ursina import *

ITERATIONS = 8

class Spring:
    def __init__(self, mass = 5, force = 50, damping = 4, speed = 4):
        self.target = Vec3()
        self.position = Vec3()
        self.velocity = Vec3()

        self.mass = mass
        self.force = force
        self.damping = damping
        self.speed = speed

    def shove(self, force):
        x, y, z = force.x, force.y, force.z

        if x != x:
            x = 0
        if y != y:
            y = 0
        if z != z:
            z = 0

        self.velocity = self.velocity + Vec3(x, y, z)

    def update(self, dt):
        scaledDeltaTime = min(dt,1) * self.speed / ITERATIONS

        for i in range(ITERATIONS):
            iterationForce = self.target - self.position
            acceleration = (iterationForce * self.force) / self.mass

            acceleration = acceleration - self.velocity * self.damping

            self.velocity = self.velocity + acceleration * scaledDeltaTime
            self.position = self.position + self.velocity * scaledDeltaTime

        return self.position