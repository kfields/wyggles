import numpy as np
import arcade
from PIL import Image

from wyggles.engine import *

class Dna:
    def __init__(self, klass):
        self.klass = klass
        self.name = sprite_engine.gen_id(klass.__name__)
        self.kind = klass.__name__.lower()

    def create_texture(self, surface, imgName, imgsize):
        # image = Image.new('RGBA', imgsize, (255, 0, 0, 0)) #Create the image
        #image = Image.frombuffer("RGBA",( surface.get_width(), surface.get_height() ), surface.get_data(), "raw", "RGBA", 0, 1)
        data = surface.get_data()
        # convert bgra to rgba
        a = np.frombuffer(data, dtype=np.uint8)
        a.shape = (-1, 4)
        data = a[:,[2,1,0,3]].tobytes()
        #
        image = Image.frombuffer("RGBA", imgsize, data, "raw", "RGBA", 0, 1)
        return arcade.Texture(imgName, image)
