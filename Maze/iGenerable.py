from abc import ABC, abstractmethod

from Maze.cell import Cell
from Utility.enums import Direction
from Utility.enums import Instruction
from Utility.enums import Border
from Utility.enums import Color
from Interface.GUI.tkController import TkController

class IGenerable(ABC):
    def __init__(self, output: TkController, width: int, height: int):
        """Generate a perfect maze with columns(width) and rows(height) 
        """
        
        self.width = width
        self.height = height
        
        # Maze resides in cells
        self.cells = [[Cell(x,y) for y in range(height)] for x in range(width)]
        
        # List of coordinates we have visited or not
        self.visited = []
        self.unvisited = [] 
        
        # Possible Directions (Up), (Down), (Left), (Right)
        # Directions as x,y coordinates
        self.dir_coords = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        # The graphic output display
        self.window = output
        
    @abstractmethod
    def generate(self) -> list[list[Cell]]:
        """Utilize the algorithm instance to create a 2d list of Cell with a given width x height
        """
        pass
    
    def _fill_unvisited(self) -> list[(int,int)]:
        """Algorithms that keep track of unvisited cells will need an initial reference to all maze cells
        """
        
        # Create a list and add all cell addresses
        lst = []
        for y in range(self.height):
            for x in range(self.width):
                lst.append((x,y))
        return lst
    
    def _get_cell(self, address: tuple[int,int]) -> Cell:
        return self.cells[address[0]][address[1]]
    
    def _add_cell(self, address: tuple[int,int]) -> None:
        """Add address (x,y) to visited and remove from unvisited
        """
        
        if address not in self.visited:
            self.visited.append(address)
            
        if address in self.unvisited:
            self.unvisited.remove(address)
        
        # Cells added to maze are denoted as white squares    
        self.window.animator.draw_frame(address, Instruction.CELL, Color.WHITE)
        
    def _cut_path(self, first: tuple[int,int], second: tuple[int,int]) -> None:
        """Remove walls between two cells first (x,y) and second (x,y)
        """
        
        # Get the direction we came from
        dir = self.__get_direction(first, second)
        
        # Since we are traveling in reverse we can interpret this is as coming from [dir]
        if dir == Direction.UP.value:
            # Remove walls from maze
            self._get_cell(first).bottom = 0
            self._get_cell(second).top = 0
            
            # Remove walls from graphic output
            self.window.animator.queue_frame(first, Instruction.BORDER, Border.BOTTOM)
            self.window.animator.queue_frame(second, Instruction.BORDER, Border.TOP)
        elif dir == Direction.DOWN.value:
            self._get_cell(first).top = 0
            self._get_cell(second).bottom = 0

            self.window.animator.queue_frame(first, Instruction.BORDER, Border.TOP)
            self.window.animator.queue_frame(second, Instruction.BORDER, Border.BOTTOM)
        elif dir == Direction.LEFT.value:
            self._get_cell(first).right = 0
            self._get_cell(second).left = 0

            self.window.animator.queue_frame(first, Instruction.BORDER, Border.RIGHT)
            self.window.animator.queue_frame(second, Instruction.BORDER, Border.LEFT)
        elif dir == Direction.RIGHT.value:
            self._get_cell(first).left = 0
            self._get_cell(second).right = 0
            
            self.window.animator.queue_frame(first, Instruction.BORDER, Border.LEFT)
            self.window.animator.queue_frame(second, Instruction.BORDER, Border.RIGHT)
            
        self.window.animator.draw_pending()
        
    def __get_direction(self, first: tuple[int,int], second: tuple[int,int]) -> int:      
        """Return an index for the direction of travel between first (x,y) and second (x,y)
        """       
        dir = first[0] - second[0], first[1] - second[1]
        return self.dir_coords.index(dir)