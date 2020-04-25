import math
import random

from PIL import Image
import cairo
from pyglet import clock
 
from wyggles.engine import *
from wyggles.beacon import *

from wyggles import Dna
from wyggles.assets import asset
from wyggles import Sprite, SpriteFactory

PI = math.pi
RADIUS = 32
WIDTH = RADIUS
HEIGHT = RADIUS

class FruitDna(Dna):
    def __init__(self, klass):
        super().__init__(klass)
        self.textures = []
        self.drawArray()

    def drawArray(self):
        #surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        filename = asset("images/" + self.kind + ".png")
        #print(filename)
        surface = cairo.ImageSurface.create_from_png(filename)

        ctx = cairo.Context(surface)
        ctx.scale(1, 1)  # Normalizing the canvas

        imgsize = (RADIUS, RADIUS) #The size of the image

        #
        self.textures.append(self.create_texture(surface, f"{self.kind}_0", imgsize))

        for y in range(2):
            for x in range(2):
                self.drawBite(ctx, x * 32, y * 32)
                self.textures.append(self.create_texture(surface, f"{self.kind}_{x+y}", imgsize))

    def drawBite(self, ctx, x, y):
        ctx.arc(x, y, 16, 0, PI * 2)
        ctx.close_path()
        #pat = cairo.SolidPattern(0, 0, 0, alpha=0)
        #ctx.set_source(pat)
        ctx.set_operator(cairo.Operator.CLEAR)
        ctx.fill()


#
class Fruit(Sprite):
    def __init__(self, layer, dna):
        super().__init__(layer, dna)
        self.type = dna.kind
        self.energy = 5
        self.beacon = Beacon(self, self.type)
        sprite_engine.addBeacon(self.beacon)
        self.texture = dna.textures[0]

    def receive_munch(self):
        self.energy -= 1
        if(self.energy <= 0):
            self.hide()
            sprite_engine.removeBeacon(self.beacon)
            self.layer.remove_sprite(self)
            return 0.01
        #else
        self.texture = self.dna.textures[5 - self.energy]
        return 0.01

    def is_munched(self):
        return self.energy == 0


class Apple(Fruit):
    def __init__(self, layer):
        super().__init__(layer, FruitDna(self.__class__))


class Banana(Fruit):
    def __init__(self, layer):
        super().__init__(layer, FruitDna(self.__class__))


class Grape(Fruit):
    def __init__(self, layer):
        super().__init__(layer, FruitDna(self.__class__))


class Orange(Fruit):
    def __init__(self, layer):
        super().__init__(layer, FruitDna(self.__class__))


class Pineapple(Fruit):
    def __init__(self, layer):
        super().__init__(layer, FruitDna(self.__class__))


class Strawberry(Fruit):
    def __init__(self, layer):
        super().__init__(layer, FruitDna(self.__class__))



class FruitFactory(SpriteFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def create_random(self):
        return list(kinds.values())[random.randint(0, 5)](self.layer)

    def setup(self):
        for sprite in self.layer.sprites:
            model = Fruit.create(sprite.position, sprite)
            self.layer.add_model(model)

kinds = {
    'apple': Apple,
    'banana': Banana,
    'grape': Grape,
    'orange': Orange,
    'pineapple': Pineapple,
    'strawberry': Strawberry
}