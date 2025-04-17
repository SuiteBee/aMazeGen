class Cell: 
    def __init__(self, x, y):
        # Cell coordinates in the maze (0,0) is bottom left (n,n) is top right
        self.x = x
        self.y = y
        
        self.top = 1
        self.bottom = 1
        self.left = 1
        self.right = 1
        self.visited = False