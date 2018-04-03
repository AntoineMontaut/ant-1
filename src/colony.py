class Colony():
    def __init__(self, pos):
        self.type = 'colony'
        self.mass = 0.
        self.pos = pos
        self.width = 20
        self.height = 20
        self.color = (0, 255, 0, 128)

    def get_position(self):
        return self.pos

    def get_dimensions(self):
        return (self.width, self.height)

    def get_color(self):
        return self.color
