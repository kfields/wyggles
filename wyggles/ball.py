
import math
import pymunk

from wyggles.sprite.sprite import Sprite
from wyggles.sprite.engine import *
from wyggles.sprite.body import *
from wyggles.sprite.beacon import *

class Ball(Sprite):
    def __init__(self, layer):
        super().__init__(layer)
        self.setSize(22,22)        
        self.type = 'ball'
        self.name = spriteEngine.genId(self.type) ;                
        self.createSprite(self.name, self.type)
        #
        self.beacon = Beacon(self, self.type)
        spriteEngine.addBeacon(self.beacon)
        #
        mass = 1
        radius = 11
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        spriteEngine.space.add(body, shape)
        self.body = body

    def receiveKick(self, angle, distance):
        strength = 20
        px = (math.cos(angle*degRads))*strength
        py = (math.sin(angle*degRads))*strength
        self.body.apply_impulse_at_local_point( (px, py), (0, 0) )
