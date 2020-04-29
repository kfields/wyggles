import math
import random

import numpy as np
import arcade

from wyggles.sprite import Sprite
from wyggles.engine import *
from wyggles.beacon import *
from .dna import WyggleDna

from .brains.default import DefaultWyggleBrain
#BRAIN = DefaultWyggleBrain
from .brains.proto import ProtoBrain
BRAIN = ProtoBrain

PI = math.pi
RADIUS = 32
WIDTH = RADIUS
HEIGHT = RADIUS

class WyggleSeg(Sprite):
    def __init__(self, layer, dna):
        super().__init__(layer)
        self.dna = dna
        self.next = None
        self.track = None
        self.track_ndx = 0
        self.track_max = 256
        self.on_track = False

    def put_on_track(self, track):
        self.track = track
        self.on_track = True
        self.materialize_at(track[self.track_ndx*2], track[self.track_ndx*2+1])

    def on_update(self, delta_time: float = 1/60):
        super().on_update(delta_time)

    def move(self):

        self.set_pos(self.track[self.track_ndx*2], self.track[self.track_ndx*2+1])    
        self.track_ndx += 1
        if self.track_ndx >= self.track_max:
            self.track_ndx = 0

        #else if there is a next segment and not on the track yet...
        if(self.next and self.track_ndx > 16):
              self.next.put_on_track(self.track)


class WyggleTail(WyggleSeg):
    def __init__(self, layer, dna):
        super().__init__(layer, dna)
        self.name = sprite_engine.gen_id(self.kind)                
        self.texture = self.dna.tail_texture
        
class WyggleHead(WyggleSeg):
    def __init__(self, layer, dna):
        super().__init__(layer, dna)
        self.face = 'happy'

    def move_to(self, position):
        self.track[self.track_ndx * 2] = position[0]
        self.track[self.track_ndx * 2 + 1] = position[1]
        self.move()
        for seg in self.segs:
            if seg.on_track:
                seg.move()

    def happy_face(self):
        self.face = 'happy'
        self.texture = self.dna.happy_face_texture

    def munchy_face(self):
        self.face = 'munchy'
        self.texture = self.dna.munchy_face_texture

    def open_mouth(self):
        self.munchy_face()

    def close_mouth(self):
        self.happy_face()
#
class Wyggle(WyggleHead):
    @classmethod
    def create():
        pass
    def __init__(self, layer):
        super().__init__(layer, WyggleDna(Wyggle))
        self.name = sprite_engine.gen_id(self.kind)
        self.brain = BRAIN(self)
        self.length_max = 6
        self.segs = []
        self.texture = self.dna.happy_face_texture

        self.track = [0] * self.track_max*2
        self.length = 1
        self.butt = None

        for i in range(self.length_max-1):
            self.grow()

    def grow(self):
        length = len(self.segs)
        if(length >= self.length_max):
            return
        seg = WyggleTail(self.layer, self.dna)
        self.segs.append(seg)
        self.length = length = len(self.segs)
        seg.z = -.001 * length
        
        was_butt = self.butt
        self.butt = seg
        if(was_butt != None):
            was_butt.next = self.butt 
        else:
            self.next = self.butt 
    