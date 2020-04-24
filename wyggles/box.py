
import math
 
from wyggles.sprite import Sprite
from wyggles.engine import *
from wyggles.body import *

class Box(Sprite):
    def __init__(self, layer):
        Sprite.__init__(self, layer)
        self.setSize(64,64)      
        self.type = 'box'
        self.name = sprite_engine.gen_id(self.type)                
        self.load_texture('images/box')
        #
        self.body = BoxBody(self)
        self.body.setSize(64,64,1000)
        sprite_engine.addBody(self.body)

    def receive_kick(self, angle, distance):
        px = distance*(math.cos(angle*degRads))
        py = distance*(math.sin(angle*degRads))        
        self.body.addForce(px, py)
