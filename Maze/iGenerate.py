from abc import ABC, abstractmethod
from Maze.cell import Cell
from Draw.plot import Plot

class IGenerate(ABC):
    def __init__(self, width: int, height: int, isAnimated: bool):
        """isAnimated will introduce a timestep to visualize the generation of the maze
        """
        
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
        self.plot = Plot(width, height, isAnimated)
        
    @abstractmethod
    def generate(self) -> list[list[Cell]]:
        """Utilize the algorithm instance create and return a 2d list of Cell with a given width x height
        
        Return 2d list of Cell to represent maze
        """
        pass
    
    def __fill_unvisited(self) -> list[(int,int)]:
        arr = []
        for x in range(self.width):
            for y in range(self.height):
                arr.append((x,y))
        return arr