class Wall():
    """a wall object is just a wrapper for a Rect"""
    def __init__(self, rect):
        self.mass = float('inf')
        self.rect = rect