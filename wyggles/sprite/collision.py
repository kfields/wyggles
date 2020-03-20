
import math
from wyggles.mathutils import *

class Collision():
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2
        self.contactX = 0
        self.contactY = 0
        self.normalX = 0
        self.normalY = 0
        self.separation = 0
        #
        self.numContacts = 2
        self.contacts = [] * self.numContacts
        i = 0            
        while(i < self.numContacts):
            self.contacts.append(Contact())
            i = i + 1            
        #
        self.touched = False ;

    def collide(self):
        #spriteConsole.write("Collision.collide:") ;
        if(self.touched):
            return
        #
        shapeType1 = self.b1.shapeType
        shapeType2 = self.b2.shapeType
        #
        if(shapeType1 == 'ball'):
            if(shapeType2 == 'ball'):
                return self.collideBallBall(self.b1, self.b2)
            elif(shapeType2 == 'box'):
                return self.collideBallBox(self.b1, self.b2)
        elif(shapeType1 == 'box'):
            if(shapeType2 == 'ball'):
                return self.collideBallBox(self.b2, self.b1)
            elif(shapeType2 == 'box'):
                return self.collideBoxBox(self.b2, self.b1)        
        
    def collideBallBall(self, b1, b2):
        radialDistance = b1.radius + b2.radius
        x1 = b1.x 
        y1 = b1.y
        x2 = b2.x 
        y2 = b2.y
        dist = distance2d(x1,y1,x2,y2)
        if(dist < radialDistance):
            self.normalX = (x2 - x1) / dist
            self.normalY = (y2 - y1) / dist
            self.contactX = x1 + self.normalX * b1.radius
            self.contactY = y1 + self.normalY * b1.radius
            self.separation = radialDistance - dist
            self.mergeContact()
            return True

        self.touched = False        
        return False

    def collideBallBox(self, b1, b2):
        inside = b2.contains(b1)
        
        for edge in b2.edges:
            if(edge.intersectBall(b1, self, inside)):
                self.mergeContact()
                return True

        self.touched = False
        return False

    def collideBoxBox(self, b1, b2):
        inside = b2.contains(b1)
        for edge in b2.edges:
            if(edge.intersectBox(b1, self, inside)):
                self.mergeContact()
                return True
        self.touched = False
        return False

    def mergeContact(self):
        self.touched = True                
        c = None
        cInsert = None
        i = 0
        for c in self.contacts:
            if(c.touched):
                continue
            if(c.x == self.contactX and c.y == self.contactY):
                cInsert = c
                break
            if(c.touched == False):
                cInsert = c
                #break ;
        #
        if(cInsert == None):
            return
        #else
        #
        cInsert.x = self.contactX
        cInsert.y = self.contactY
        cInsert.normalX = self.normalX
        cInsert.normalY = self.normalY
        cInsert.separation = self.separation
        cInsert.touched = True
    
    def preStep(self, inv_dt):
        k_allowedPenetration = 0.01
        k_biasFactor = 0.8
        b1 = self.b1
        b2 = self.b2
        c = None
        i = 0
        for c in self.contacts:
            if(not c.touched):
                continue
            #Vec2 r1 = c->position - body1->position;
            r1x = c.x - b1.x
            r1y = c.y - b1.y            
            #Vec2 r2 = c->position - body2->position;
            r2x = c.x - b2.x
            r2y = c.y - b2.y                
            #Precompute normal mass, tangent mass, and bias.
            #dot = a.x * b.x + a.y * b.y;
            #float rn1 = Dot(r1, c->normal);
            rn1 = r1x * c.normalX + r1y * c.normalY
            #float rn2 = Dot(r2, c->normal);
            rn2 = r2x * c.normalX + r2y * c.normalY
            
            #float kNormal = body1->invMass + body2->invMass;
            kNormal = b1.invMass + b2.invMass
            
            #kNormal += body1->invI * (Dot(r1, r1) - rn1 * rn1) + body2->invI * (Dot(r2, r2) - rn2 * rn2);
            r1Dot = r1x * r1x + r1y * r1y
            r2Dot = r2x * r2x + r2y * r2y
            
            kNormal += b1.invI * (r1Dot - rn1 * rn1) + b2.invI * (r2Dot - rn2 * rn2)
            
            #c->massNormal = 1.0f / kNormal
            c.massNormal = 1.0 / kNormal
    
            #skip friction for now...
            #...
            
            #c->bias = -k_biasFactor * inv_dt * Min(0.0f, c->separation + k_allowedPenetration);
            c.bias = -k_biasFactor * inv_dt * min(0.0, c.separation + k_allowedPenetration)
    
            #Apply normal + friction impulse
            #Vec2 P = c->Pn * c->normal + c->Pt * tangent;
            #f6:skipping friction
            pX = c.Pn * c.normalX
            pY = c.Pn * c.normalY
            #body1->velocity -= body1->invMass * P;
            b1.velX -= b1.invMass * pX
            b1.velY -= b1.invMass * pY
            
            #body1->angularVelocity -= body1->invI * Cross(r1, P);
            #cross = a.x * b.y - a.y * b.x;
            r1Cross = r1x * pY - r1y * pX
            b1.angularVel -= b1.invI * r1Cross
    
            #body2->velocity += body2->invMass * P;
            b2.velX += b2.invMass * pX
            b2.velY += b2.invMass * pY
            
            #body2->angularVelocity += body2->invI * Cross(r2, P);
            r2Cross = r2x * pY - r2y * pX
            b1.angularVel += b2.invI * r2Cross
    
            #Initialize bias impulse to zero.
            #c->Pnb = 0.0f;
            c.Pnb = 0.0

    def applyImpulse(self):
        b1 = self.b1
        b2 = self.b2
        i = 0
        for c in self.contacts:
            if(not c.touched):
                continue    
            #c->r1 = c->position - b1->position;
            c.r1X = c.x - b1.x
            c.r1Y = c.y - b1.y
            #if(isNaN(c.r1X)) alertOnce('c.r1X') ;
            #c->r2 = c->position - b2->position;
            c.r2X = c.x - b2.x
            c.r2Y = c.y - b2.y
            #Relative velocity at contact
            #Vec2 dv = b2->velocity + Cross(b2->angularVelocity, c->r2) - b1->velocity - Cross(b1->angularVelocity, c->r1);
            #scalar cross(vec,vec) = a.x * b.y - a.y * b.x;
            #vec cross(scalar,vec) = (-s * a.y, s * a.x);
            a1CrossX = -b1.angularVel * c.r1Y
            a1CrossY = b1.angularVel * c.r1X
            
            a2CrossX = -b2.angularVel * c.r2Y
            a2CrossY = b2.angularVel * c.r2X
            #if(isNaN(a1CrossX)) alertOnce('a1CrossX') ;
            dvX = b2.velX + a2CrossX - b1.velX - a1CrossX
            dvY = b2.velY + a2CrossY - b1.velY - a1CrossY
            #Compute normal impulse
            #float vn = Dot(dv, c->normal);
            #dot = a.x * b.x + a.y * b.y;
            vn = dvX * c.normalX + dvY * c.normalY
            #float dPn = c->massNormal * (-vn + c->bias);
            dPn = c.massNormal * (-vn + c.bias)
            #Clamp the accumulated impulse
            #float Pn0 = c->Pn;
            Pn0 = c.Pn
            #c->Pn = Max(Pn0 + dPn, 0.0f);
            c.Pn = max(Pn0 + dPn, 0.0)
            
            #dPn = c->Pn - Pn0;
            dPn = c.Pn - Pn0
            #Apply contact impulse
            #Vec2 Pn = dPn * c->normal;
            PnX = dPn * c.normalX
            PnY = dPn * c.normalY
    
            #b1->velocity -= b1->invMass * Pn;
            b1.velX -= b1.invMass * PnX
            b1.velY -= b1.invMass * PnY
            #b1->angularVelocity -= b1->invI * Cross(c->r1, Pn);
            #scalar cross(vec,vec) = a.x * b.y - a.y * b.x;
            p1Cross = c.r1X * PnY - c.r1Y * PnX
            b1.angularVel -= b1.invI * p1Cross    
            #b2->velocity += b2->invMass * Pn;
            b2.velX += b2.invMass * PnX
            b2.velY += b2.invMass * PnY
            #b2->angularVelocity += b2->invI * Cross(c->r2, Pn);
            p2Cross = c.r2X * PnY - c.r2Y * PnX
            b2.angularVel += b2.invI * p2Cross    
            #f6:skip friction
            #...
    def postStep(self):
        self.touched = False
        for c in self.contacts:
            c.touched = False ;

class Contact():
    def __init__(self):
        #Contact() : Pn(0.0f), Pt(0.0f), Pnb(0.0f) {}
        #Vec2 position;
        self.x = 0
        self.y = 0
        #Vec2 normal;
        self.normalX = 0
        self.normalY = 0
        #Vec2 r1, r2;
        self.r1X = 0
        self.r1Y = 0
        self.r2X = 0
        self.r2Y = 0
        #float separation;
        self.separation = 0
        #float Pn;    // accumulated normal impulse
        self.Pn = 0
        #float Pt;    // accumulated tangent impulse
        #float Pnb;    // accumulated normal impulse for position bias
        self.Pnb = 0
        #float massNormal, massTangent;
        self.massNormal = 0
        #float bias;
        self.bias = 0
        #f6:newstuff
        self.touched = False ;
