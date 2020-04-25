class Beacon():
    def __init__(self, sprite, type):
        self.sprite = sprite
        self.type = type
    '''
        self.x = 0
        self.y = 0
    def set_pos(self, x, y):
        self.x = x
        self.y = y        
    '''
    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, val):
        self.sprite.position = val

    @property
    def x(self):
        return self.sprite.position[0]

    @property
    def y(self):
        return self.sprite.position[1]
