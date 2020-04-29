import math
from .mathutils import *
from botsley.run.agent import Agent

class Brain(Agent):

    def __init__(self, sprite):
        super().__init__()
        self.sprite = sprite

        self.begin_pos = (0, 0)
        self.end_pos = (0, 0)
        #self.sensor_range = 512
        self.sensor_range = 128

    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, val):
        self.sprite.position = val

    @property
    def x(self):
        return self.sprite.position[0]

    @property
    def y(self):
        return self.sprite.position[1]

    def at_goal(self):
        distance = distance2d(self.position, self.end_pos)
        return distance < 5

    def move_to(self, end_pos):
        self.begin_pos = self.position
        self.end_pos = end_pos

    def project(self, distance):
        px = self.x+(distance*(math.cos(self.heading*degRads)))
        py = self.y+(distance*(math.sin(self.heading*degRads)))
        self.move_to((px, py))

    def update(self, delta_time):
        pass