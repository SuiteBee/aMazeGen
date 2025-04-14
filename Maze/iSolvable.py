from Maze.cell import Cell
from Draw.plot import Plot
from abc import ABC, abstractmethod

class ISolvable(ABC):
    def __init__(self, maze: list[Cell][Cell], isAnimated: bool):
        """Maze is a 2d list of Cell
        isAnimated will introduce a timestep to visualize the solution of the maze
        """
        self.maze = maze
        self.isAnimated = isAnimated
        
        # Maze resides in cells
        self.visited = []
        self.unvisited = []
        self.path = []
        
        # Possible Directions (Up), (Down), (Left), (Right)
        # Directions as x,y coordinates
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        
        # The visualized maze (animated will include a pause)
        self.plot = Plot(self.cells, isAnimated)
        
    
    @abstractmethod
    def solve() -> list[Cell]: 
        """Utilize the algorithm instance create and return a 2d list of Cell with a given width x height
        
        Return list of cells as solution path
        """
        pass
    