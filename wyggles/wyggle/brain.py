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
        self.focus = None
        self.state = "wanderer"
        self.consider_max = 10
        self.consider_timer = self.consider_max
        #
        self.munch_timer = 10

    def reset(self):
        self.state = ''
        self.focus = None

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)

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
        left, bottom, right, top = sprite.left, sprite.bottom, sprite.right, sprite.top
        w_left, w_bottom, w_right, w_top = world_left, world_bottom, world_right, world_top

        if(left < w_left):
            delta_x = w_left - left
            need_turn = True
        elif(right > w_right):
            delta_x = w_right - right
            need_turn = True

        if(bottom < w_bottom):
            delta_y = w_bottom - bottom
            need_turn = True
        elif(top > w_top):
            delta_y = w_top - top
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

        nextX = self.x + delta_x
        nextY = self.y + delta_y
        self.sprite.move_to((nextX, nextY))

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
