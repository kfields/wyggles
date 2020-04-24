import math
 
from wyggles.sprite import Sprite
from wyggles.engine import *
from wyggles.beacon import *

from pyglet import clock
    
class Apple(Sprite):
    def __init__(self, layer):
        Sprite.__init__(self, layer)
        self.setSize(22,22)        
        self.energy = 5
        self.type = 'apple'
        self.name = sprite_engine.gen_id(self.type)                
        self.load_texture(self.type + str(self.energy))
        #
        self.beacon = Beacon(self, self.type)
        sprite_engine.addBeacon(self.beacon)

    def __del__(self):
        pass
        
    def receive_munch(self):
        self.energy -= 1
        if(self.energy <= 0):
            self.hide()
            sprite_engine.removeBeacon(self.beacon)
            self.layer.remove_sprite(self)
            def reSpawnApple(dt, *args, **kwargs):
                layer = sprite_engine.get_root()
                apple = Apple(self.layer)
                materializeRandomFromCenter(apple)

            clock.schedule_once(reSpawnApple, 3.0)
            return
        #else
        self.load_texture(self.type + str(self.energy)) ;

    def is_munched(self):
        return self.energy == 0 
