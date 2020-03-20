import math
import os
#import random
from random import random
import sys

import pymunk

from .layer import Layer

from wyggles.mathutils import *
from .collision import Collision

worldMinX = 0 
worldMinY = 0 
worldMaxX = 1024
worldMaxY = 768

def without(source, element):
    temp = source[:]
    try:
        while temp:
            temp.remove( element )
    except:
        return temp
    return temp

def materializeRandomFromCenter(sprite):
    halfMaxX = worldMaxX / 2
    halfMaxY = worldMaxX / 2
    diameter = 400
    radius = diameter / 2
    sprite.materializeAt( (halfMaxX - radius) + (random() * diameter), (halfMaxY - radius) + (random() * diameter))        

class SpriteEngine():
    
    def __init__(self):
        self.root = Layer("root")
        #
        self.actors = []
        self.beacons = []
        self.bodies = []
        self.collisions = []
        self.idCounter = 0
        #
        self.gravityX = 0
        #self.gravityY = 9.8 ;        
        self.gravityY = 0
        # new stuff
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (self.gravityX, self.gravityY)

        
    def addActor(self, actor):
        self.actors.append(actor)
        
    def removeActor(self, actor) :
        #self.actors  = self.actors.without(actor)
        self.actors.remove(actor)
        
    def addBeacon(self, beacon) :
        self.beacons.append(beacon) ;

    def removeBeacon(self, beacon):
        #self.beacons = self.beacons.without(beacon)
        self.beacons.remove(beacon)

    def addBody(self, body):
        self.bodies.append(body)
        
    def removeBody(self, body):
        #self.bodies = self.bodies.without(body)
        self.bodies.remove(body)

    def addCollision(self, collision):
        self.collisions.append(collision)

    def removeCollision(self, collision):
        #self.collisions = self.collisions.without(collision)
        self.collisions.remove(collision)

    def findCollision(self, b1, b2):
        collision = None
        for collision in self.collisions:
            if(collision.b1 == b1 and collision.b2 == b2 or collision.b1 == b2 and collision.b2 == b1):
                return collision ;
        return None ;

    def step(self, dt):
        dt = .1 ;
        inv_dt = 0
        if(dt > 0.0):
            inv_dt = 1.0 / dt
        b = None
        #
        self.broadphase() ;
        #
        for b in self.bodies:
            if(b.invMass == 0.0):
                continue
            b.velX += dt * (self.gravityX + b.invMass * b.forceX)
            b.velY += dt * (self.gravityY + b.invMass * b.forceY)
            b.angularVel += dt * b.invI * b.torque
        #    ... insert penetration constraints here ...
        for collision in self.collisions:
            if(not collision.touched):
                 continue
            collision.preStep(inv_dt)
        #
        iterations = 1
        i = 0;
        while(i < iterations):
            i = i + 1
            for collision in self.collisions:
                if(not collision.touched):
                     continue
                collision.applyImpulse()
        #
        for collision in self.collisions:
            if(not collision.touched): 
                 continue
            collision.postStep()
        #
        for b in self.bodies:
            if(b.invMass == 0.0):
                continue
            b.setPos(b.x + dt * (b.velX + b.biasedVelX), b.y + dt * (b.velY + b.biasedVelY)) ;
            
            b.rotation += dt * (b.angularVel + b.biasedAngularVel);
    
            #Bias velocities are reset to zero each step.
            b.biasedVelX = 0
            b.biasedVelY = 0
            b.biasedAngularVel = 0
            b.forceX = 0
            b.forceY = 0
            b.torque = 0
            #
            b.step()
        #
        for actor in self.actors:
            actor.step()
        #
        #self.renderer.render()
        self.render()
            
    def broadphase(self):
        b1 = None 
        b2 = None
        for b1 in self.bodies:
          for b2 in self.bodies:
            if(b1 == b2):
                continue                
            if (b1.invMass == 0.0 and b2.invMass == 0.0):
                continue
            if(not b1.intersects(b2)):
                continue
            collision = self.findCollision(b1, b2)
            if(collision == None):
                collision = Collision(b1,b2)
                self.addCollision(collision)
            collision.collide() ;

    def query(self, x, y, distance):
        beacon = None
        result = None
        for beacon in self.beacons:
            dist = distance2d(x, y, beacon.x, beacon.y)
            if(dist < distance):
                if(result == None):
                    result = [beacon]
                else:
                    result.append(beacon)
        return result

    def genId(self, name):
        result = name + str(self.idCounter)
        self.idCounter += 1
        return result
    #
    def render(self):
        self.root.render()
        
    def get_root(self):
        return self.root    

#fixme: singleton pattern
spriteEngine = SpriteEngine()
