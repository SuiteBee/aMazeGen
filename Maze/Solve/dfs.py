import random

from Maze.iSolvable import ISolvable
from Utility.enums import Instruction
from Utility.enums import Color
from Maze.cell import Cell
from Interface.GUI.tkController import TkController

class DFS(ISolvable):
    """Depth First Search implementation
    
    Randomly visits cells as far as it can go and then backtracks when stuck
    """
    
    def __init__(self, output: TkController, maze: list[list[Cell]]):
        super().__init__(output, maze)
        
    def solve(self, start: tuple[int,int], finish: tuple[int,int]) -> list[Cell]: 
        self.start_address = start
        self.finish_address = finish
        
        # Begin search from starting cell
        current_cell = self._get_cell(self.start_address)
        
        # Visit random unvisited neighbors until we reach the finish address
        while current_cell.address != self.finish_address:
            # Visit this cell
            self.__visit(current_cell)

            # Get next cell and repeat
            current_cell = self._get_next(current_cell)        
        
        # Visit the final cell
        self.__visit(current_cell)
        
        # Color and set our solution to return
        self.solution = self.__get_solution()
        
        return self.solution
    
    def __get_solution(self) -> list[Cell]:
        """Color and return a list of cells in our path
        """
        
        shortest_path = []
        while len(self.path) > 0:
            address = self.path.pop(0)
            self.window.animator.queue_frame(address, Instruction.CELL, Color.GREEN)
            
            cell = self._get_cell(address)
            shortest_path.append(cell)
        
        # Draw everything in the frame queue
        self.window.animator.draw_pending()
        
        return shortest_path
            
    def _get_next(self, cell: Cell) -> Cell:
        """Randomly return an unvisited neighbor or backtrack to previous cell in path
        """
        
        # Get all unvisited neighbors of cell
        unv_neighbors = [neighbor for neighbor in self._get_neighbors(cell) if not neighbor.visited]
        has_unv_neighbors = len(unv_neighbors) > 0
        
        if has_unv_neighbors:
            # Search random unvisited neighbor
            return random.choice(unv_neighbors)
        else:
            # No unvisited neighbors remain backtrack and see if last cell had any
            next_address = self.path.pop()
            return self._get_cell(next_address)

    def __visit(self, cell: Cell):
        """Mark cell as visited and append to path
        """
        # Get all unvisited neighbors of cell
        unv_neighbors = [neighbor for neighbor in self._get_neighbors(cell) if not neighbor.visited]
        has_unv_neighbors = len(unv_neighbors) > 0
        
        if not cell.visited:
            # First visit add to path and color red
            cell.visited = True
            self.path.append(cell.address)
            self.window.animator.draw_frame(cell.address, Instruction.CELL, Color.RED)
        elif has_unv_neighbors:
            # Backtrack to search unvisited neighbors add to path
            self.path.append(cell.address)
        else:
            # Backtrack and no unvisited neighbors remain color pink (searched path)
           self.window.animator.draw_frame(cell.address, Instruction.CELL, Color.PINK)