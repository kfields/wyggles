import math
 
from wyggles.sprite.sprite import Sprite
from wyggles.sprite.engine import *
from wyggles.sprite.body import *
from wyggles.sprite.beacon import *

from pyglet import clock
    
class Apple(Sprite):
    def __init__(self, layer):
        Sprite.__init__(self, layer)
        self.setSize(22,22)        
        self.energy = 5
        self.type = 'apple'
        self.name = spriteEngine.genId(self.type)                
        self.createSprite(self.name, self.type + str(self.energy))
        #
        self.beacon = Beacon(self, self.type)
        spriteEngine.addBeacon(self.beacon)

    def __del__(self):
        pass
        
    def receiveMunch(self):
        self.energy -= 1
        if(self.energy <= 0):
            self.hide()
            spriteEngine.removeBeacon(self.beacon)
            self.layer.remove_sprite(self)
            def reSpawnApple(dt, *args, **kwargs):
                layer = spriteEngine.get_root()
                apple = Apple(self.layer)
                materializeRandomFromCenter(apple)

            clock.schedule_once(reSpawnApple, 3.0)
            return
        #else
        self.setImageSrc(self.type + str(self.energy)) ;

    def isMunched(self): 
        return self.energy == 0 
