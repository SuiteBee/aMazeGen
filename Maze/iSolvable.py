from abc import ABC, abstractmethod

from Maze.cell import Cell
from Utility.enums import Instruction
from Utility.enums import Color
from Interface.GUI.tkController import TkController

class ISolvable(ABC):
    """Solves a given matrix of cells containing information about their borders
    """
    
    def __init__(self, output: TkController, maze: list[list[Cell]]):
        """Maze is a 2d list of Cell
        isAnimated will introduce a timestep to visualize the solution of the maze
        """
        self.maze = maze
                
        self.start_address = None
        self.finish_address = None
        
        self.width = len(maze)
        self.height = len(maze[0])
        
        self.visited = []
        self.solution = []
        self.path = []
        
         # The graphic output display
        self.window = output
    
    @abstractmethod
    def solve(self, start: tuple[int,int], finish: tuple[int,int]) -> list[Cell]: 
        """Utilize the algorithm instance to return a solution path as list[cell]
        """
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Returns name of algorithm
        """
        pass
    
    def reset(self) -> None:
        """Reset maze to initial state
        """
        
        for y in range(self.height):
            for x in range(self.width):
                cell = self._get_cell((x,y))
                cell.reset_solution()
                
                self.window.animator.queue_frame(cell.address, Instruction.CELL, Color.WHITE)
            
        self.path = []
        self.window.animator.draw_pending()
        
    def _get_shortest_path(self, first_cell: Cell, last_cell: Cell) -> list[Cell]:
        """Color and return a chain of cells from first to last connected by Cell.parent property
        """
        
        shortest_path = []
        while last_cell.address != first_cell.address:
            # Add our last cell to the path and color it green
            shortest_path.insert(0, last_cell)
            self.window.animator.queue_frame(last_cell.address, Instruction.CELL, Color.GREEN)

            # Set our last cell to be its parent (where it came from)
            last_cell = self._get_cell(last_cell.parent)
            
        self.window.animator.queue_frame(first_cell.address, Instruction.CELL, Color.GREEN)
        self.window.animator.draw_pending()
        
        return shortest_path
    
    def _get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors = []
        
        if cell.left == 0 and not cell.address == self.start_address:
            neighbors.append(self.__get_left(cell.address))
            
        if cell.right == 0 and not cell.address == self.finish_address:
            neighbors.append(self.__get_right(cell.address))
            
        if cell.top == 0:
            neighbors.append(self.__get_above(cell.address))
            
        if cell.bottom == 0:
            neighbors.append(self.__get_below(cell.address))
            
        return neighbors
    
    def _get_cell(self, address: tuple[int,int]) -> Cell:
        return self.maze[address[0]][address[1]]
    
    def __get_left(self, address: tuple[int,int]) -> Cell:
        return self._get_cell((address[0]-1,address[1]))
    
    def __get_right(self, address: tuple[int,int]) -> Cell:
        return self._get_cell((address[0]+1,address[1]))
    
    def __get_above(self, address: tuple[int,int]) -> Cell:
        return self._get_cell((address[0],address[1]+1))
    
    def __get_below(self, address: tuple[int,int]) -> Cell:
        return self._get_cell((address[0],address[1]-1))
    
    