import math

floatMax = 1E400

degRads = (math.pi*2)/360

def distance2d(start, end):
    diffX = start[0] - end[0]
    diffY = start[1] - end[1]
    return math.sqrt((diffX * diffX) + (diffY * diffY))

def sign(x):
    if(x < 0.0):
        return -1.0
    else:
        return 1.0
