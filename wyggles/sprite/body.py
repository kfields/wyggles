from .edge import *
from wyggles.mathutils import *

class Body():
    def __init__(self):
        self.sprite = None
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.forceX = 0
        self.forceY = 0
        #
        self.rotation = 0
        self.angularVel = 0
        self.biasedVelX = 0
        self.biasedVelY = 0
        self.biasedAngularVel = 0
        self.torque = 0
        #
        self.dimX = 0
        self.dimY = 0
        #
        self.halfWidth = 0
        self.halfHeight = 0
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0                    
        #
        self.friction = 0
        self.mass = 0
        self.invMass = 0
        self.I = 0
        self.invI = 0        

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.validate()

    def setMinMax(self, minX, minY, maxX, maxY, mass):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
        #        
        self.dimX = maxX - minX
        self.dimY = maxY - minY
        self.setMass(mass)
        #
        self.halfWidth = self.dimX / 2
        self.halfHeight = self.dimY / 2                
        self.x = minX +  self.halfWidth
        self.y = minY + self.halfHeight
        #
        self.validate()

    def setSize(self, width, height, mass):
        self.dimX = width
        self.dimY = height
        self.setMass(mass)
        self.halfWidth = self.dimX / 2
        self.halfHeight = self.dimY / 2

    def validate(self):
        self._validate()

    def _validate(self):
        self.minX = self.x - self.halfWidth
        self.minY = self.y - self.halfHeight
        self.maxX = self.x + self.halfWidth
        self.maxY = self.y + self.halfHeight                

    def setMass(self, mass):
        self.mass = mass ;
        
        if (mass < floatMax):
            self.invMass = 1.0 / mass
            self.I = mass * (self.dimX * self.dimX + self.dimY * self.dimY) / 12.0
            self.invI = 1.0 / self.I
        else:
            self.invMass = 0.0 ;
            self.I = floatMax ;
            self.invI = 0.0 ;

    def addForce(self, x, y):
        self.forceX += x
        self.forceY += y

    def step(self):
        self.sprite._setPos(self.x, self.y)

    def intersects(self, body):
        if(self.minX > body.maxX):
            return False
        if(self.minY > body.maxY):
            return False
        if(body.minX > self.maxX):
          return False
        if(body.minY > self.maxY):
            return False        
        return True

    def contains(self, body):
        if(body.minX < self.minX):
          return False
        if(body.minY < self.minY):
          return False
        if(body.maxX > self.maxX):
            return False
        if(body.maxY > self.maxY):
            return False        
        return True

    def overlaps(self, body):
        return self.intersects(body) or self.contains(body) or body.contains(self)
#/////
class BallBody(Body):
    def __init__(self, sprite):
        Body.__init__(self)
        self.sprite = sprite
        self.shapeType = 'ball'
    def validate(self):
        self._validate()
        self.radius = self.halfWidth
#/////
class BoxBody(Body):
    def __init__(self, sprite):
        Body.__init__(self)
        self.sprite = sprite        
        self.shapeType = 'box'
        self.edges = [Edge(), Edge(), Edge(), Edge()]
    def validate(self):
        self._validate()
        self.edges[0].setPoints(self.minX, self.minY, self.minX, self.maxY)
        self.edges[1].setPoints(self.minX, self.maxY, self.maxX, self.maxY)
        self.edges[2].setPoints(self.maxX, self.maxY, self.maxX, self.minY)
        self.edges[3].setPoints(self.maxX, self.minY, self.minX, self.minY)
