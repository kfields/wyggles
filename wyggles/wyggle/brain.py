import math
import random
import arcade

import wyggles.app
from wyggles.mathutils import *
from wyggles.engine import *
import wyggles.app
from wyggles.brain import Brain
from wyggles.fruit import Fruit

class WyggleBrain(Brain):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.heading = random.randint(0, 359)
        self.wheel = 0

        self.state = "wanderer"
        self.consider_max = 10
        self.consider_timer = self.consider_max
        self.focus = None
        #
        self.munch_timer = 10

    def change_state(self, state):
        self.state = state

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

    def move(self):
        x, y = self.position
        to_x, to_y = self.end_pos

        pd = random.randint(0, 3)
        if pd == 0:
            self.micro_left()
        elif pd == 2:
            self.micro_right()

        steering_ndx = int(math.pi + (math.atan2(y - to_y, x - to_x)))
        delta = steering[steering_ndx][self.wheel]

        self.try_move(delta)

    
    def try_move(self, delta):
        delta_x, delta_y = delta
        next_x, next_y = 0, 0
        need_turn = False

        sprite = self.sprite
        pos = sprite.position
        min_x, min_y, max_x, max_y = sprite.left, sprite.bottom, sprite.right, sprite.top
        w_min_x, w_min_y, w_max_x, w_max_y = world_min_x, world_min_y, world_max_x, world_max_y

        if(min_x < w_min_x):
            delta_x = w_min_x - min_x
            need_turn = True
        elif(max_x > w_max_x):
            delta_x = w_max_x - max_x
            need_turn = True

        if(min_y < w_min_y):
            delta_y = w_min_y - min_y
            need_turn = True
        elif(max_y > w_max_y):
            delta_y = w_max_y - max_y
            need_turn = True

        #TODO:use pymunk
        '''
        if not need_turn:
            landscape_layer = wyggles.app.landscape_layer
            if landscape_layer:
                need_turn = len(arcade.check_for_collision_with_list(self.sprite, landscape_layer)) != 0
        '''
        if(need_turn):
            self.right(45)
            #self.randforward()
            self.project(self.sensor_range)

        nextX = self.getX() + delta_x
        nextY = self.getY() + delta_y
        #
        self.sprite.track[self.sprite.track_ndx * 2] = nextX
        self.sprite.track[self.sprite.track_ndx * 2 + 1] = nextY
        self.sprite._move()

    def left(self, angle):
        heading = self.heading - angle
        self.heading = heading if heading > 0 else 360 + heading

    def right(self, angle):
        heading = self.heading + angle
        self.heading = heading if heading < 359 else heading - 360

    def micro_left(self):
        ph = self.wheel - 1
        if ph < 0:
            ph = 0
        self.wheel = ph

    def micro_right(self):
        ph = self.wheel + 1
        if ph > 2:
            ph = 2
        self.wheel = ph

    def forward(self, distance):
        x, y = self.position
        px = x + (distance * (math.cos(self.heading * degRads)))
        py = y + (distance * (math.sin(self.heading * degRads)))
        self.move_to((px, py))

    def randforward(self):
        self.forward(random.randint(0, self.sensor_range))

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
            self.change_state("eater")
        self.move()

    def eat(self):
        self.sprite.stop()
        if self.focus.is_munched():
            self.sprite.close_mouth()
            self.sprite.energy = self.sprite.energy + self.focus.energy
            self.change_state("wanderer")
            self.focus = None
            self.sprite.go()
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
            self.change_state('wanderer') 

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
        self.change_state("hunter")
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
        self.change_state("kicker")
        return True


steering = [
    [(1, -1), (1, 0), (1, 1)],
    [(1, 0), (1, 1), (0, 1)],
    [(1, 1), (0, 1), (-1, 1)],
    [(0, 1), (-1, 1), (-1, 0)],
    [(-1, 1), (-1, 0), (-1, -1)],
    [(-1, 0), (-1, -1), (0, -1)],
    [(-1, -1), (0, -1), (1, -1)],
    [(0, -1), (1, -1), (1, 0)],
]
