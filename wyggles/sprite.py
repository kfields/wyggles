import math
import arcade
import arcade

from pyglet import image
from wyggles.mathutils import *

class Sprite(arcade.Sprite):
    def __init__(self, layer, dna=None):
        super().__init__()
        self.dna = dna
        self.kind = self.__class__.__name__
        self.layer = layer
        self.brain = None
        self.body = None
        self.beacon = None
        self.heading = 0
        self._z = 0
        #
        self.energy = 5
        #
        layer.add_sprite(self)

    @property
    def x(self):
        return self.center_x

    @x.setter
    def x(self, val):
        self.center_x = val

    @property
    def y(self):
        return self.center_y

    @y.setter
    def y(self, val):
        self.center_y = val

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, val):
        self._z = val
        self.layer.depth_sort()

    def on_update(self, delta_time: float = 1/60):
        if self.brain:
            self.brain.update(delta_time)
        if self.body:
            self.position = self.body.position
            self.angle = math.degrees(self.body.angle)

    def load_texture(self, imgName):
        filename = 'assets/' + imgName + ".png"
        self.imgSrc = filename
        self.texture = arcade.load_texture(filename)
        
    def set_pos(self, x, y):
        self.position = (x,y)
        if(self.body != None):
            self.body.position = x, y

    def set_origin(self, x, y):
        self.set_pos(x, y)
        self.fromX = x
        self.fromY = y        
        self.toX = x
        self.toY = y        

    def intersects(self, sprite):
        if(self.left > sprite.right):
            return False
        if(self.bottom > sprite.top):
            return False
        if(sprite.left > self.right):
            return False
        if(sprite.bottom > self.top):
            return False        
        return True

    def show(self):
        pass

    def hide(self):
        pass

    def materialize_at(self, x, y):
        self.set_origin(x, y)
        self.show()
    
    def move(self):
        pass


class SpriteFactory:
    def __init__(self, layer):
        self.layer = layer
