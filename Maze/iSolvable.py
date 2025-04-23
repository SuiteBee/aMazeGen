from Maze.cell import Cell
from Draw.tkDraw import TkDraw
from abc import ABC, abstractmethod

class ISolvable(ABC):
    def __init__(self, output: TkDraw, maze: list[list[Cell]]):
        """Maze is a 2d list of Cell
        isAnimated will introduce a timestep to visualize the solution of the maze
        """
        self.maze = maze
                
        self.start = None
        self.finish = None
        
        self.width = len(maze[0])
        self.height = len(maze)
        
        self.visited = []
        self.solution = []
        self.path = []
        
        # Possible Directions (Up), (Down), (Left), (Right)
        # Directions as x,y coordinates
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        
         # The graphic output display
        self.window = output
    
    @abstractmethod
    def solve(self, start: tuple[int,int], finish: tuple[int,int]) -> list[Cell]: 
        """Utilize the algorithm instance to return a solution path as list[cell]
        """
        pass
    
    def _get_cell(self, address: tuple[int,int]) -> Cell:
        return self.maze[address[0]][address[1]]
    
    def _get_left(self, address: tuple[int,int]) -> Cell:
        return self._get_cell((address[0]-1,address[1]))
    
    def _get_right(self, address: tuple[int,int]) -> Cell:
        return self._get_cell((address[0]+1,address[1]))
    
    def _get_above(self, address: tuple[int,int]) -> Cell:
        return self._get_cell((address[0],address[1]+1))
    
    def _get_below(self, address: tuple[int,int]) -> Cell:
        return self._get_cell((address[0],address[1]-1))