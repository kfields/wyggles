
import math

class Edge():
    
    def __init__(self):
        pass
    def setPoints(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1        
        self.x2 = x2
        self.y2 = y2
        #
        diffX = x2 - x1
        diffY = y2 - y1
        self.length = math.sqrt((diffX*diffX)+(diffY*diffY))
        
        self.dirX = diffX / self.length
        self.dirY = diffY / self.length
    
        nx = -self.dirY
        ny = self.dirX        
        
        self.normalX = nx
        self.normalY = ny
        
    def closestPoint(self, x, y, collision):
        px = x - self.x1
        py = y - self.y1
        #distance along v0-v1 of closest point on line to point.
        dist = px * self.dirX + py * self.dirY
        if(dist < 0):
            dist = 0.0
        elif(dist > self.length):
            dist = self.length
        
        closestX = self.x1 + dist * self.dirX
        closestY = self.y1 + dist * self.dirY
        diffX = x - closestX
        diffY = y - closestY
        collision.contactX = closestX
        collision.contactY = closestY
        return math.sqrt((diffX*diffX)+(diffY*diffY))      
        #return math.abs(math.sqrt((diffX*diffX)+(diffY*diffY))) ;

    def intersectLine(self, a2x, a2y, b2x, b2y):
        a1x = self.x1
        a1y = self.y1
        b1x = self.x2
        b1y = self.y2
                
        A = a2x - a1x
        B = b2x - a2x
        C = b1x - a1x
        
        D = a1y - a2y
        E = b1y - a1y
        F = b2y - a2y

        if F == 0:
            return False

        s = (A + B*D/F) / (C - B * E / F)
            
        if ( (s < 0.0) or (s > 1.0) ):
            return False
        
        t = (D + s * E ) / F
        if ( (t < 0.0) or (t > 1.0) ):
            return False
        
        return True    

    def intersectBall(self, b1, collision, inside):
        collide = False
        x = b1.x
        y = b1.y
        radius = b1.radius
        separation = 0 ;
        dist = self.closestPoint(x, y, collision)
        
        dx0 = x - collision.contactX
        dy0 = y - collision.contactY
        if(dx0 * self.normalX + dy0 * self.normalY > 0):
          side = 1
        else:
          side = -1
        if(inside):
            x1 = b1.x + (-b1.velX * 1000)
            y1 = b1.y + (-b1.velY * 1000)
            x2 = b1.x
            y2 = b1.y
            collide = self.intersectLine(x1, y1, x2, y2)
            #separation = -(dist + radius) ;
            #separation = dist - radius ;
        else:
            #separation = dist - radius ;
            collide = side == 1 and dist < radius
        #if (dist < radius || inside) {            
        if(collide):            
            #penetration
            collision.normalX = self.normalX
            collision.normalY = self.normalY
            collision.separation = dist - radius
            return True            
        return False

    def intersectBox(self, b1, collision, inside):
        collide = False
        x = b1.x
        y = b1.y
        radius = b1.halfWidth
        separation = 0
        dist = self.closestPoint(x, y, collision)
        #
        dx0 = x - collision.contactX
        dy0 = y - collision.contactY

        if(dx0 * self.normalX + dy0 * self.normalY > 0):
          side = 1
        else:
          side = -1
        if(inside):
            x1 = b1.x + (-b1.velX * 1000)
            y1 = b1.y + (-b1.velY * 1000)
            x2 = b1.x
            y2 = b1.y
            collide = self.intersectLine(x1, y1, x2, y2)
            #separation = -(dist + radius) ;
            #separation = dist - radius ;
        else:
            #separation = dist - radius ;
            collide = side == 1 and dist < radius
        #if (dist < radius || inside) {            
        if(collide):            
            #penetration
            collision.normalX = self.normalX
            collision.normalY = self.normalY
            collision.separation = dist - radius
            return True ;            
        return False ;
