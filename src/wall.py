class Wall():
    """a wall object is just a wrapper for a Rect"""
    def __init__(self, rect, colony=False):
        # self.mass = float('inf')
        self.type = 'wall'
        self.mass = 9999999
        self.rect = rect
        self.colony = colony
