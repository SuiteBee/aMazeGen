from Maze.iSolvable import ISolvable
from Utility.enums import Instruction
from Utility.enums import Color
from Maze.cell import Cell
from Interface.GUI.tkController import TkController

class BFS(ISolvable):
    """Breadth First Search implementation
    
    Solves by visiting neighbors of cells in the path first
    """
    
    def __init__(self, output: TkController, maze: list[list[Cell]]):
        super().__init__(output, maze)
        
    def solve(self, start: tuple[int,int], finish: tuple[int,int]) -> list[Cell]: 
        self.start_address = start
        self.finish_address = finish
        
        # Insert our starting address to the queue
        self.path.insert(0, self.start_address)
        
        # As it is a queue, we can check the last item to see if we have found the exit
        while self.path[-1] != self.finish_address:
            # Get our next cell to examine from the queue
            current_address = self.path.pop()
            current_cell = self._get_cell(current_address)
            
            # Visit all neighbors and record current cell as their parent
            self.__expand_search(current_cell)
            
            # Draw everything in the frame queue
            self.window.animator.draw_pending()
    
        # Extract the shortest path
        first_cell = self._get_cell(self.start_address)
        last_cell = self._get_cell(self.finish_address)
        self.solution = self._get_shortest_path(first_cell, last_cell)
        
        return self.solution
    
    def __expand_search(self, cell: Cell) -> None:
        """Visit all unvisited neighbors of cell and record cell as their parent
        """
        unv_neighbors = [neighbor for neighbor in self._get_neighbors(cell) if not neighbor.visited]

        # Visit unvisited neighbors
        for unv in unv_neighbors or []:
            self.__visit(unv, cell)
      
        # Color our examined cell pink as it is no longer at the forefront of the search
        self.window.animator.queue_frame(cell.address, Instruction.CELL, Color.PINK)
                    

    def __visit(self, cell: Cell, origin: Cell):
        """Visit cell, set parent(origin) and add to queue
        """
        cell.visited = True
        cell.parent = origin.address
        self.path.insert(0, cell.address)
        
        # Color our cell red to denote it is the next cell to be examined
        self.window.animator.queue_frame(cell.address, Instruction.CELL, Color.RED)