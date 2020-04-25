import math
import random

import numpy as np
import arcade

from wyggles.sprite import Sprite
from wyggles.engine import *
from wyggles.beacon import *
from .dna import WyggleDna
from .brain import WyggleBrain

PI = math.pi
RADIUS = 32
WIDTH = RADIUS
HEIGHT = RADIUS

class WyggleSeg(Sprite):
    def __init__(self, layer, dna):
        super().__init__(layer)
        self.dna = dna
        self.next = None
        self.track_ndx = 0
        #self.track_max = 132
        self.track_max = 256
        self.onTrack = False
        self.track = None
        self.stopped = False

    def stop(self):
        self.stopped = True

    def go(self):
        self.stopped = False

    def put_on_track(self, track):
        self.track = track
        self.onTrack = True
        self.materialize_at(track[self.track_ndx*2], track[self.track_ndx*2+1])

    def on_update(self, delta_time: float = 1/60):
        if self.onTrack:
            self.move()
        super().on_update(delta_time)

    def move(self):
        if self.stopped:
            return
        self._move()

    def _move(self):
        self.set_pos(self.track[self.track_ndx*2], self.track[self.track_ndx*2+1])    
        self.track_ndx += 1
        if(self.track_ndx >= self.track_max):
            self.track_ndx = 0
        if(self.next == None):
            return #early out.
        #else if there is a next segment and not on the track yet...
        if(self.track_ndx > 16):
              self.next.put_on_track(self.track)
        return True


class WyggleTail(WyggleSeg):
    def __init__(self, layer, dna):
        super().__init__(layer, dna)
        self.name = sprite_engine.gen_id(self.kind)                
        self.texture = self.dna.tail_texture
        
class WyggleHead(WyggleSeg):
    def __init__(self, layer, dna):
        super().__init__(layer, dna)
        self.face = 'happy'

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
        self.brain = WyggleBrain(self)
        self.length_max = 6
        self.segs = []
        self.pre_load()
        self.texture = self.dna.happy_face_texture

        self.track = [0] * self.track_max*2
        self.length = 1
        self.butt = None

        self.grow()
        self.grow()
        self.grow()
        self.grow()
        self.grow()
        #

    def stop(self):
        super().stop()
        for seg in self.segs:
            seg.stop()

    def go(self):
        super().go()
        for seg in self.segs:
            seg.go()

    def pre_load(self):
        pass

    def grow(self):
        length = len(self.segs)
        if(length == self.length_max):
            return
        seg = WyggleTail(self.layer, self.dna)
        self.segs.append(seg)
        length = len(self.segs)
        self.length = length
        #seg.z = -length
        seg.z = -.001 * length
        
        was_butt = self.butt
        self.butt = seg
        if(was_butt != None):
            was_butt.next = self.butt 
        else:
            self.next = self.butt 
    