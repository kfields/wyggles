import math
import random
from PIL import Image
import cairo

from wyggles import Dna

PI = math.pi

RADIUS = 32
WIDTH = RADIUS
HEIGHT = RADIUS

class WyggleDna(Dna):
    def __init__(self, klass):
        super().__init__(klass)
        name = self.name
        r = random.uniform(0, .75)
        r1 = r + .20
        r2 = r + .25
        g = random.uniform(0, .75)
        g1 = g + .20
        g2 = g + .25
        b = random.uniform(0, .75)
        b1 = b + .20
        b2 = b + .25       
        self.color1 = r,g,b,1
        self.color2 = r1,g1,b1,1
        self.color3 = r2,g2,b2,1
        #
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(surface)
        #ctx.scale(1, 1)  # Normalizing the canvas

        imgsize = (RADIUS, RADIUS) #The size of the image

        self.draw_segment(ctx)
        self.tail_texture = self.create_texture(surface, name + 'tail', imgsize)

        #Eating
        self.draw_munchy_face(ctx)
        self.munchy_face_texture = self.create_texture(surface, name + 'munchy_face', imgsize)
        #Sad
        self.draw_happy_face(ctx, -1)
        self.sadFaceImage = self.create_texture(surface, name + 'sadFace', imgsize)
        #Neutral
        self.draw_happy_face(ctx, 0)
        self.neutralFaceImage = self.create_texture(surface, name + 'neutralFace', imgsize)
        #Happy
        self.draw_happy_face(ctx, 1)
        self.happy_face_texture = self.create_texture(surface, name + 'happy_face', imgsize)
        #
        self.face_texture = self.happy_face_texture

    def draw_segment(self, ctx):
        r1, g1, b1, a1 = self.color1
        r2, g2, b2, a2 = self.color2
        r3, g3, b3, a3 = self.color3
        pat = cairo.RadialGradient(16,16,16, 8,8,4)
        pat.add_color_stop_rgba(1, r3, g3, b3, a3)
        pat.add_color_stop_rgba(0.9, r2, g2, b2, a2)
        pat.add_color_stop_rgba(0, r1, g1, b1, a1)

        ctx.arc(16, 16, 12, 0, PI*2)
        ctx.close_path()

        ctx.set_source(pat)
        ctx.fill()

    def draw_happy_face(self, ctx, valence):
        self.draw_face(ctx)
        #Mouth
        x0 = 8
        y0 = 20 - (4 * valence)
        x1 = 16
        y1 = 26 + (4 * valence)
        x2 = 24
        y2 = y0
        #
        #ctx.move_to(x0, y0)
        ctx.curve_to(x0, y0, x1, y1, x2, y2)
        ctx.set_line_width(2)
        ctx.set_source_rgb(255, 0, 0) #red
        ctx.stroke()

    def draw_munchy_face(self, ctx):
        self.draw_face(ctx)
        #Mouth
        ctx.arc(16, 16, 8, PI, 2 * PI)
        ctx.close_path()
        ctx.set_source_rgb(255, 0, 0) #red
        ctx.fill()

    def draw_face(self, ctx):
        self.draw_segment(ctx)
        #Eyes - Whites
        ctx.arc(8, 8, 4, 0, PI*2)
        ctx.arc(24, 8, 4, 0, PI*2) 
        ctx.close_path()
        ctx.set_source_rgb(255, 255, 255)
        ctx.fill()
        #Eyes - Darks
        ctx.arc(8, 8, 2, 0, PI*2)
        ctx.arc(24, 8, 2, 0, PI*2) 
        ctx.close_path()
        ctx.set_source_rgb(0,0,0)
        ctx.fill()

