
import math
 
from wyggles.sprite.sprite import Sprite
from wyggles.sprite.engine import *
from wyggles.sprite.body import *

class Box(Sprite):
    def __init__(self, layer):
        Sprite.__init__(self, layer)
        self.setSize(64,64)      
        self.type = 'box'
        self.name = spriteEngine.genId(self.type)                
        self.createSprite(self.name, self.type)
        #
        self.body = BoxBody(self)
        self.body.setSize(64,64,1000)
        spriteEngine.addBody(self.body)

    def receiveKick(self, angle, distance):
        px = distance*(math.cos(angle*degRads))
        py = distance*(math.sin(angle*degRads))        
        self.body.addForce(px, py)
