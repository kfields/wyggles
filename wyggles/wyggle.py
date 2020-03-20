import math
from random import random, randint, uniform

from PIL import Image
import cairo
import numpy as np
import arcade

from wyggles.sprite.sprite import Sprite
from wyggles.sprite.engine import *
from wyggles.sprite.body import *
from wyggles.sprite.beacon import *

PI = math.pi
RADIUS = 32
WIDTH = RADIUS
HEIGHT = RADIUS

class WiggleDna:
    def __init__(self, sprite):
        self.name = name = spriteEngine.genId(sprite.__class__.__name__)
        r = uniform(0, .75)
        r1 = r + .20
        r2 = r + .25
        g = uniform(0, .75)
        g1 = g + .20
        g2 = g + .25
        b = uniform(0, .75)
        b1 = b + .20
        b2 = b + .25       
        self.color1 = r,g,b,1
        self.color2 = r1,g1,b1,1
        self.color3 = r2,g2,b2,1
        #
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(surface)
        ctx.scale(1, 1)  # Normalizing the canvas

        self.drawSegment(ctx)
        self.tailTexture = self.create_texture(surface, name + 'tail')

        #Eating
        self.drawMunchyFace(ctx)
        self.munchyFaceTexture = self.create_texture(surface, name + 'munchyFace')
        #Sad
        self.drawHappyFace(ctx, -1)
        self.sadFaceImage = self.create_texture(surface, name + 'sadFace')
        #Neutral
        self.drawHappyFace(ctx, 0)
        self.neutralFaceImage = self.create_texture(surface, name + 'neutralFace')
        #Happy
        self.drawHappyFace(ctx, 1)
        self.happyFaceTexture = self.create_texture(surface, name + 'happyFace')
        #
        self.faceTexture = self.happyFaceTexture

    def create_texture(self, surface, imgName):
        imgsize = (RADIUS, RADIUS) #The size of the image
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

    def drawSegment(self, ctx):
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

    def drawHappyFace(self, ctx, valence):
        self.drawFace(ctx)
        #Mouth
        x0 = 8
        y0 = 22 - (4 * valence)
        x1 = 16
        y1 = 26 + (4 * valence)
        x2 = 24
        y2 = y0
        #
        ctx.move_to(x0, y0)
        ctx.curve_to(x0, y0, x1, y1, x2, y2)
        ctx.set_line_width(2)
        ctx.set_source_rgb(255, 0, 0) #red
        ctx.stroke()

    def drawMunchyFace(self, ctx):
        self.drawFace(ctx)
        #Mouth
        ctx.arc(16, 16, 8, PI, 2 * PI)
        ctx.close_path()
        ctx.set_source_rgb(255, 0, 0) #red
        ctx.fill()

    def drawFace(self, ctx):
        self.drawSegment(ctx)
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

class WyggleSeg(Sprite):
    def __init__(self, layer, dna):
        super().__init__(layer)
        self.dna = dna
        self.setSize(32,32)
        self.next = None
        self.trackNdx = 0
        #self.trackMax = 132
        self.trackMax = 256
        self.onTrack = False
        self.track = None
        self.stopped = False

    def stop(self):
        self.stopped = True

    def go(self):
        self.stopped = False

    def putOnTrack(self, track):
        self.track = track
        self.onTrack = True
        self.materializeAt(track[self.trackNdx*2], track[self.trackNdx*2+1])

    def on_update(self, delta_time: float = 1/60):
        if self.onTrack:
            self.move()
        super().on_update(delta_time)

    def move(self):
        if self.stopped:
            return
        self._move()

    def _move(self):
        self.setPos(self.track[self.trackNdx*2], self.track[self.trackNdx*2+1])    
        self.trackNdx += 1
        if(self.trackNdx >= self.trackMax):
            self.trackNdx = 0
        if(self.next == None):
            return #early out.
        #else if there is a next wig and not on the track yet...
        if(self.trackNdx > 16):
              self.next.putOnTrack(self.track)
        return True

#
class WyggleTail(WyggleSeg):
    def __init__(self, layer, dna):
        super().__init__(layer, dna)
        self.name = spriteEngine.genId(self.kind)                
        self.texture = self.dna.tailTexture
        
#########
wigglySteering = [
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

    def happyFace(self):
        self.face = 'happy'
        self.texture = self.dna.happyFaceTexture

    def munchyFace(self):
        self.face = 'munchy'
        self.texture = self.dna.munchyFaceTexture

    def openMouth(self):
        self.munchyFace()

    def closeMouth(self):
        self.happyFace()
#
class Wyggle(WyggleHead):
    @classmethod
    def create():
        pass
    def __init__(self, layer):
        super().__init__(layer, WiggleDna(self))
        self.name = spriteEngine.genId(self.kind)
        self.lengthMax = 6 
        self.segs = []
        self.preLoad()
        self.texture = self.dna.happyFaceTexture
        self.sensorRange = 128
        self.wheel = 0
        self.state = 'wanderer'
        #
        #self.segs.append(self)
        self.track = [0] * self.trackMax*2
        self.length = 1
        self.butt = None
        #
        self.considerMax = 10
        self.considerTimer = self.considerMax
        self.focus = None
        #
        self.munchTimer = 10
        #
        self.grow()
        self.grow()
        self.grow()
        self.grow()
        self.grow()
        #
        spriteEngine.addActor(self)

    def stop(self):
        super().stop()
        for seg in self.segs:
            seg.stop()

    def go(self):
        super().go()
        for seg in self.segs:
            seg.go()

    def preLoad(self):
        pass

    def grow(self):
        length = len(self.segs)
        if(length == self.lengthMax):
            return
        seg = WyggleTail(self.layer, self.dna)
        self.segs.append(seg)
        length = len(self.segs)
        self.length = length
        #seg.setZ(-length)
        seg.setZ(-.001 * length)
        
        wasButt = self.butt
        self.butt = seg
        if(wasButt != None):
            wasButt.next = self.butt 
        else:
            self.next = self.butt 

    def changeState(self, state):
        self.state = state

    def microLeftTurn(self):
        ph = self.wheel - 1
        if(ph < 0 ):
            ph = 0
        self.wheel = ph 

    def microRightTurn(self):
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
        if(self.atGoal()):
            pt = math.floor(random()*3)
            pd = math.floor(random()*45)
            if(pt == 0):
                self.turnLeft(pd)
            elif(pt == 2):
                self.turnRight(pd)
            else:
                pass
            self.project(self.sensorRange)
        self.move()
        self.consider()

    def hunt(self):
        if(self.intersects(self.focus)):
            self.changeState('eater')
        self.move()
        self.consider()

    def eat(self):
        self.stop()
        if(self.focus.isMunched()):
            self.closeMouth() 
            self.energy = self.energy + self.focus.energy
            self.changeState('wanderer')
            self.go()
            # self.grow()
            return
        #else
        self.munch()

    def munch(self):
        if(self.munchTimer > 0):
            self.munchTimer -=1 
            return
        else:
            self.munchTimer = 10
            
        if(self.face != 'munchy'):
            self.openMouth()
        else:
            self.closeMouth()
            self.focus.receiveMunch()

    def kick(self):
        self.moveTo(self.focus.x, self.focus.y) #fixme: add--> follow(sprite)
        if(self.intersects(self.focus)):
            self.focus.receiveKick(self.heading, self.sensorRange)            
        elif(distance2d(self.x, self.y, self.focus.x, self.focus.y) > self.sensorRange):
            self.changeState('wanderer') 
        self.move()

    def move(self):
        x = self.getX()
        y = self.getY()        
        steeringNdx = 0
        bCompass = math.pi+(math.atan2(y - self.toY, x - self.toX))
        if(bCompass != 0):
            steeringNdx = 8 - int(round(bCompass/self.octant))
        if(steeringNdx < 0):
            steeringNdx = 0            
        elif(steeringNdx > 7):
            steeringNdx = 7
        #
        pd = math.floor(random()*3)
        #
        if(pd == 0):
            self.microLeftTurn() 
        elif(pd == 2):
            self.microRightTurn() 
        else:
            pass
        #
        steeringNdx = steeringNdx*6
        steeringNdx = steeringNdx + (self.wheel * 2)
        #
        deltaX = wigglySteering[steeringNdx]
        deltaY = wigglySteering[steeringNdx + 1]

        self.tryMove(deltaX, deltaY)

    def tryMove(self, deltaX, deltaY):
        nextX = 0
        nextY = 0
        needTurn = False
        #
        if(self.minX < worldMinX):
            deltaX = -self.minX
            needTurn = True
        elif(self.maxX > worldMaxX):
            deltaX = worldMaxX - self.maxX
            needTurn = True
        #
        if(self.minY < worldMinY):
            deltaY = worldMinY - self.minY
            needTurn = True
        elif(self.maxY > worldMaxY):
            deltaY = worldMaxY - self.maxY
            needTurn = True
        #        
        if(needTurn):
            self.turnRight(45)
            self.project(self.sensorRange)
        #
        nextX = self.getX() + deltaX
        nextY = self.getY() + deltaY                    
        #
        self.track[self.trackNdx*2] = nextX
        self.track[self.trackNdx*2+1] = nextY
        self._move()

    def consider(self):
        if(self.considerTimer > 0):
            self.considerTimer -= 1
            return 
        #else
        self.considerTimer = self.considerMax
        beacons = spriteEngine.query(self.x, self.y, self.sensorRange)
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
            if(beacon.type == 'apple'):
                apple = beacon.sprite
                break
        #
        if(apple == None):
            return False
        #else
        self.focus = apple
        self.moveTo(apple.x, apple.y)
        self.changeState('hunter')
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
        self.moveTo(ball.x, ball.y)
        self.changeState('kicker')
        return True
