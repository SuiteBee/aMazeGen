from abc import ABC, abstractmethod
from Maze.cell import Cell
from Draw.tkController import TkController

class ISolvable(ABC):
    def __init__(self, output: TkController, maze: list[list[Cell]]):
        """Maze is a 2d list of Cell
        isAnimated will introduce a timestep to visualize the solution of the maze
        """
        self.maze = maze
                
        self.start_address = None
        self.finish_address = None
        
        self.width = len(maze[0])
        self.height = len(maze)
        
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
    
    def reset(self) -> None:
        """Reset maze to initial state
        """
        
        for y in range(self.height):
            for x in range(self.width):
                cell = self._get_cell((x,y))
                cell.reset_solution()
                
                self.window.animator.queue_frame(cell.address, ("cell", "white"))
            
        self.path = []
        self.window.animator.draw_pending()
    
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
    
    