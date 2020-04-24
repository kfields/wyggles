import math
import pymunk

from wyggles.assets import asset
from wyggles.sprite import Sprite
from wyggles.engine import *
from wyggles.beacon import *

class Ball(Sprite):
    def __init__(self, layer):
        super().__init__(layer)
        self.setSize(32,32)
        self.type = 'ball'
        self.name = sprite_engine.gen_id(self.type)
        self.load_texture('images/ball')
        #
        self.beacon = Beacon(self, self.type)
        sprite_engine.addBeacon(self.beacon)
        #
        mass = 1
        radius = 16
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = .5
        shape.friction = .9
        sprite_engine.space.add(body, shape)
        self.body = body

    def receive_kick(self, angle, distance):
        strength = 20
        px = (math.cos(angle*degRads))*strength
        py = (math.sin(angle*degRads))*strength
        self.body.apply_impulse_at_local_point( (px, py), (0, 0) )
