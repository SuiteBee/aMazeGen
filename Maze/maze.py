from Maze.cell import Cell
from Draw.plot import Plot
from abc import ABC, abstractmethod

class Maze(ABC):
    def __init__(self, width, height, isAnimated):
        # Input
        self.width = width
        self.height = height
        self.isAnimated = isAnimated
        
        # Maze resides in cells
        self.cells = [[Cell() for y in range(height)] for x in range(width)]
        self.visited = []
        self.unvisited = self.__fill_unvisited()
        self.path = []
        
        # Possible Directions (Up), (Down), (Left), (Right)
        # Directions as x,y coordinates
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        
        # The visualized maze (animated will include a pause)
        self.plot = Plot(self.cells, isAnimated)
        
    @abstractmethod
    def generate():
        pass
    
    #@abstractmethod
    #def solve():
    #    pass
    
    def __fill_unvisited(self):
        arr = []
        for x in range(self.width):
            for y in range(self.height):
                arr.append((x,y))
        return arr
    