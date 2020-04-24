import math
import data
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
        self.x = 0
        self.y = 0
        self.z = 0
        #
        self.halfWidth = 0
        self.halfHeight = 0
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0        
        #
        self.energy = 5
        #
        self.octant = (math.pi*2)/8
        #                
        layer.add_sprite(self)

    def on_update(self, delta_time: float = 1/60):
        if self.brain:
            self.brain.update(delta_time)
        if self.body:
            self.x = self.body.position.x
            self.y = self.body.position.y
            self.angle = math.degrees(self.body.angle)

        self.position = [self.x, self.y]


    def load_texture(self, imgName):
        filename = 'assets/' + imgName + ".png"
        self.imgSrc = filename
        self.texture = arcade.load_texture(filename)
        
    def set_pos(self, x, y):
        self._set_pos(x,y)
        if(self.body != None):
            self.body.position = x, y

    def _set_pos(self, x, y):
        self.x = x
        self.y = y
        #
        self.validate()

    def validate(self):
        self._validate()

    def _validate(self):
        self.min_x = self.x - self.halfWidth
        self.min_y = self.y - self.halfHeight
        self.max_x = self.x + self.halfWidth
        self.max_y = self.y + self.halfHeight
        #
        if(self.beacon != None):
            self.beacon.set_pos(self.x, self.y)

    def set_origin(self, x, y):
        self.set_pos(x, y)
        self.fromX = x
        self.fromY = y        
        self.toX = x
        self.toY = y        

    def setZ(self, z):
        self.z = z
        self.layer.depth_sort()

    def getZ(self):
        return self.z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setSize(self, width, height):
        self.halfWidth = width / 2
        self.halfHeight = height / 2

    def intersects(self, sprite):
        if(self.min_x > sprite.max_x):
            return False
        if(self.min_y > sprite.max_y):
            return False
        if(sprite.min_x > self.max_x):
            return False
        if(sprite.min_y > self.max_y):
            return False        
        return True

    def show(self):
        pass

    def hide(self):
        pass

    def materialize_at(self, x, y):
        self.set_origin(x, y)
        self.show()

    def turn_left(self, angleDelta):
        angle = self.heading - angleDelta
        if(angle < 0):
            self.heading = 360+angle
        else:
            self.heading = angle

    def turn_right(self, angleDelta):
        angle = self.heading + angleDelta
        if(angle > 359):
            self.heading = angle-360
        else:
            self.heading = angle
    
    def move(self):
        pass


class SpriteFactory:
    def __init__(self, layer):
        self.layer = layer
