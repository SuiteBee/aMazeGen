class Cell: 
    def __init__(self, x, y):
        # Cell coordinates in the maze (0,0) is bottom left (n,n) is top right
        self.x = x
        self.y = y
        self.address = (x,y)
        
        # For solution
        self.top = 1
        self.bottom = 1
        self.left = 1
        self.right = 1
        
        self.visited = False
        self.parent = None
        self.distance = None
        
    def reset_generation(self) -> None:
        """Reset cell back to state prior to generation (walls)
        """
        self.top = 1
        self.bottom = 1
        self.left = 1
        self.right = 1
        
    def reset_solution(self) -> None:
        """Reset cell back to state prior to solving
        """
        self.visited = False
        self.parent = None
        self.distance = None