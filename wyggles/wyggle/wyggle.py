import math
import random

import numpy as np
import arcade

from wyggles.sprite import Sprite
from wyggles.engine import *
from wyggles.beacon import *
from .dna import WyggleDna
from wyggles.fruit import Fruit

PI = math.pi
RADIUS = 32
WIDTH = RADIUS
HEIGHT = RADIUS

class WyggleSeg(Sprite):
    def __init__(self, layer, dna):
        super().__init__(layer)
        self.dna = dna
        self.setSize(32,32)
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

#
class WyggleTail(WyggleSeg):
    def __init__(self, layer, dna):
        super().__init__(layer, dna)
        self.name = sprite_engine.gen_id(self.kind)                
        self.texture = self.dna.tail_texture
        
#########
wiggly_steering = [
    0, -1,
    1, -1,
    1, 0,
    #
    -1, -1,
    0, -1,
    1, -1,
    #
    -1, 0,
    -1, -1,
    0, -1,
    #
    -1, 1,
    -1, 0,
    -1, -1,
    #
    0, 1,
    -1, 1,
    -1, 0,
    #
    1, 1,
    0, 1,
    -1, 1,
    #
    1, 0,
    1, 1,
    0, 1,
    #
    1, -1,
    1, 0,
    1, 1
]
#
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
        self.length_max = 6
        self.segs = []
        self.pre_load()
        self.texture = self.dna.happy_face_texture
        self.sensor_range = 128
        self.wheel = 0
        self.state = 'wanderer'
        #
        #self.segs.append(self)
        self.track = [0] * self.track_max*2
        self.length = 1
        self.butt = None
        #
        self.consider_max = 10
        self.consider_timer = self.consider_max
        self.focus = None
        #
        self.munch_timer = 10
        #
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
        #seg.setZ(-length)
        seg.setZ(-.001 * length)
        
        was_butt = self.butt
        self.butt = seg
        if(was_butt != None):
            was_butt.next = self.butt 
        else:
            self.next = self.butt 

    def change_state(self, state):
        self.state = state

    def micro_left_turn(self):
        ph = self.wheel - 1
        if(ph < 0 ):
            ph = 0
        self.wheel = ph 

    def micro_right_turn(self):
        ph = self.wheel + 1
        if(ph > 2):
            ph = 2
        self.wheel = ph 

    def on_update(self, delta_time: float = 1/60):
        super().on_update(delta_time)
        state = self.state
        if(state == 'wanderer'):
            self.wander()
        elif(state == 'hunter'):
            self.hunt() 
        elif(state == 'eater'):
            self.eat()
        elif(state == 'kicker'):
            self.kick()

    def wander(self):
        if(self.at_goal()):
            pt = math.floor(random.random()*3)
            pd = math.floor(random.random()*45)
            if(pt == 0):
                self.turn_left(pd)
            elif(pt == 2):
                self.turn_right(pd)
            else:
                pass
            self.project(self.sensor_range)
        self.move()
        self.consider()

    def hunt(self):
        if(self.intersects(self.focus)):
            self.change_state('eater')
        self.move()
        self.consider()

    def eat(self):
        self.stop()
        if(self.focus.is_munched()):
            self.close_mouth() 
            self.energy = self.energy + self.focus.energy
            self.change_state('wanderer')
            self.go()
            # self.grow()
            return
        #else
        self.munch()

    def munch(self):
        if(self.munch_timer > 0):
            self.munch_timer -=1 
            return
        else:
            self.munch_timer = 10
            
        if(self.face != 'munchy'):
            self.open_mouth()
        else:
            self.close_mouth()
            self.focus.receive_munch()

    def kick(self):
        self.move_to(self.focus.x, self.focus.y) #fixme: add--> follow(sprite)
        if(distance2d(self.x, self.y, self.focus.x, self.focus.y) < 32):
            self.focus.receive_kick(self.heading, self.sensor_range)
        '''          
        elif(distance2d(self.x, self.y, self.focus.x, self.focus.y) > self.sensor_range):
            self.change_state('wanderer') 
        '''
        self.move()

    def move(self):
        x = self.getX()
        y = self.getY()        
        steering_ndx = 0
        compass = math.pi+(math.atan2(y - self.toY, x - self.toX))
        if(compass != 0):
            steering_ndx = 8 - int(round(compass/self.octant))
        if(steering_ndx < 0):
            steering_ndx = 0            
        elif(steering_ndx > 7):
            steering_ndx = 7
        #
        pd = math.floor(random.random()*3)
        #
        if(pd == 0):
            self.micro_left_turn() 
        elif(pd == 2):
            self.micro_right_turn() 
        else:
            pass
        #
        steering_ndx = steering_ndx*6
        steering_ndx = steering_ndx + (self.wheel * 2)
        #
        delta_x = wiggly_steering[steering_ndx]
        delta_y = wiggly_steering[steering_ndx + 1]

        self.tryMove(delta_x, delta_y)

    def tryMove(self, delta_x, delta_y):
        nextX = 0
        nextY = 0
        need_turn = False
        #
        if(self.min_x < world_min_x):
            delta_x = -self.min_x
            need_turn = True
        elif(self.max_x > world_max_x):
            delta_x = world_max_x - self.max_x
            need_turn = True
        #
        if(self.min_y < world_min_y):
            delta_y = world_min_y - self.min_y
            need_turn = True
        elif(self.max_y > world_max_y):
            delta_y = world_max_y - self.max_y
            need_turn = True
        #        
        if(need_turn):
            self.turn_right(45)
            self.project(self.sensor_range)
        #
        nextX = self.getX() + delta_x
        nextY = self.getY() + delta_y                    
        #
        self.track[self.track_ndx*2] = nextX
        self.track[self.track_ndx*2+1] = nextY
        self._move()

    def consider(self):
        if(self.consider_timer > 0):
            self.consider_timer -= 1
            return 
        #else
        self.consider_timer = self.consider_max
        beacons = sprite_engine.query(self.x, self.y, self.sensor_range)
        #
        state = self.state
        if(state == 'wanderer'):
            if(not self.considerEating(beacons)):
                self.considerKicking(beacons)
        elif(state == 'hunter'):
            pass
        elif(state == 'eater'):
            pass
        elif(state == 'kicker'):
            pass
        #cleanup
        if(beacons != None):
            del beacons

    def considerEating(self, beacons):
        if(beacons == None):
            return False
        #else
        apple = None
        for beacon in beacons:  
            if(isinstance(beacon.sprite, Fruit)):
                apple = beacon.sprite
                break
        #
        if(apple == None):
            return False
        #else
        self.focus = apple
        self.move_to(apple.x, apple.y)
        self.change_state('hunter')
        return True

    def considerKicking(self, beacons):
        if(beacons == None):
            return False
        #else
        ball = None 
        for beacon in beacons:
            if(beacon.type == 'ball'):
                ball = beacon.sprite
                break
        #
        if(ball == None):
            return False
        #else
        self.focus = ball
        self.move_to(ball.x, ball.y)
        self.change_state('kicker')
        return True
