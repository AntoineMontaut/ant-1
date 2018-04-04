from pygame import Rect

class Colony():
    def __init__(self, pos):
        self.type = 'colony'
        self.mass = 0.
        self.pos = pos
        self.width = 50
        self.height = 50
        self.color = (0, 255, 0, 128)

        self.rect = Rect(self.pos[0] - self.width/2,
                        self.pos[1] - self.height/2,
                        self.width, self.height)

    def get_position(self):
        return self.pos

    def get_dimensions(self):
        return (self.width, self.height)

    def get_color(self):
        return self.color
