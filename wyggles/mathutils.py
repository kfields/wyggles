import math

floatMax = 1E400

degRads = (math.pi*2)/360 ;

def distance2d(x1, y1, x2, y2):
    diffX = x1 - x2 ;
    diffY = y1 - y2 ;
    return math.sqrt((diffX*diffX)+(diffY*diffY))    

def sign(x):
    if(x < 0.0):
        return -1.0
    else:
        return 1.0
