import math
import random
import arcade

import wyggles.app
from wyggles.mathutils import *
from wyggles.engine import *
import wyggles.app
from wyggles.wyggle.brain import WyggleBrain
from wyggles.fruit import Fruit

class DefaultWyggleBrain(WyggleBrain):
    def __init__(self, sprite):
        super().__init__(sprite)

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        state = self.state
        if state == "wanderer":
            self.wander()
        elif state == "hunter":
            self.hunt()
        elif state == "eater":
            self.eat()
        elif state == "kicker":
            self.kick()
        self.consider()

    def wander(self):
        if self.at_goal():
            pt = math.floor(random.random() * 3)
            pd = math.floor(random.random() * 45)
            if pt == 0:
                self.left(pd)
            elif pt == 2:
                self.right(pd)
            else:
                pass
            self.project(self.sensor_range)
        self.move()

    def hunt(self):
        if self.sprite.intersects(self.focus):
            self.state = "eater"
        self.move()

    def eat(self):
        if self.focus.is_munched():
            self.sprite.close_mouth()
            self.sprite.energy = self.sprite.energy + self.focus.energy
            self.state = "wanderer"
            self.focus = None
            # self.sprite.grow()
            return
        # else
        self.munch()

    def munch(self):
        if self.munch_timer > 0:
            self.munch_timer -= 1
            return
        else:
            self.munch_timer = 10

        if self.sprite.face != "munchy":
            self.sprite.open_mouth()
        else:
            self.sprite.close_mouth()
            self.focus.receive_munch()

    def kick(self):
        self.move_to(self.focus.position)  # fixme: add--> follow(sprite)
        if distance2d(self.position, self.focus.position) < 32:
            self.focus.receive_kick(self.heading, self.sensor_range)

        elif(distance2d(self.position, self.focus.position) > self.sensor_range):
            self.focus = None
            self.state = 'wanderer'

        self.move()

    def consider(self):
        if self.consider_timer > 0:
            self.consider_timer -= 1
            return
        else:
            self.consider_timer = self.consider_max

        beacons = sprite_engine.query(self.x, self.y, self.sensor_range)
        #
        state = self.state
        if state == "wanderer":
            if not self.considerEating(beacons):
                self.considerKicking(beacons)
        elif state == "hunter":
            pass
        elif state == "eater":
            pass
        elif state == "kicker":
            pass
        # cleanup
        if beacons != None:
            del beacons

    def considerEating(self, beacons):
        apple = None
        for beacon in beacons:
            if isinstance(beacon.sprite, Fruit):
                apple = beacon.sprite
                break
        #
        if apple == None:
            return False
        # else
        self.focus = apple
        self.move_to(apple.position)
        self.state = "hunter"
        return True

    def considerKicking(self, beacons):
        ball = None
        for beacon in beacons:
            if beacon.type == "ball":
                ball = beacon.sprite
                break
        #
        if ball == None:
            return False
        # else
        self.focus = ball
        self.move_to(ball.position)
        self.state = "kicker"
        return True
