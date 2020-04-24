class Beacon():
    def __init__(self, sprite, type):
        self.sprite = sprite
        self.type = type
        self.x = 0
        self.y = 0
    def set_pos(self, x, y):
        self.x = x
        self.y = y        
