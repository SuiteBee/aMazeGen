from Maze.iSolvable import ISolvable
from Maze.cell import Cell
from Draw.tkController import TkController
import random

class DFS(ISolvable):
    def __init__(self, output: TkController, maze: list[list[Cell]]):
        super().__init__(output, maze)
        
    def solve(self, start: tuple[int,int], finish: tuple[int,int]) -> list[Cell]: 
        self.start_address = start
        self.finish_address = finish
        
        # Begin search from starting cell
        start_cell = self._get_cell(self.start_address)
        self.__recursive_depth_search(start_cell)
        
        # Color and set our solution to return
        self.solution = self.__get_solution()
        
        return self.solution
    
    def __get_solution(self) -> list[Cell]:
        """Color and return a list of cells in our path
        """
        
        shortest_path = []
        while len(self.path) > 0:
            address = self.path.pop(0)
            self.window.animator.queue_frame(address, ("cell", "green"))
            
            cell = self._get_cell(address)
            shortest_path.append(cell)
        
        # Draw everything in the frame queue
        self.window.animator.draw_pending()
        
        return shortest_path
        
    def __recursive_depth_search(self, cell: Cell) -> None:
        """Recursively visit random unvisited neighbors until we reach the finish address
        """
        
        # Current cell is the exit, visit the final cell and return
        if cell.address == self.finish_address:
            self.__visit(cell, False)
            return

        # Get all unvisited neighbors of cell
        unv_neighbors = [neighbor for neighbor in self._get_neighbors(cell) if not neighbor.visited]
        has_unv_neighbors = len(unv_neighbors) > 0

        # Visit this cell
        self.__visit(cell, has_unv_neighbors)
        
        if has_unv_neighbors:
            # Search random unvisited neighbor
            next_cell = random.choice(unv_neighbors)
            self.__recursive_depth_search(next_cell)
        else:
            # No unvisited neighbors remain backtrack and see if last cell had any
            next_address = self.path.pop()
            next_cell = self._get_cell(next_address)
            self.__recursive_depth_search(next_cell)

    def __visit(self, cell: Cell, has_unv_neighbors: bool):
        """Mark cell as visited and append to path
        """
        if not cell.visited:
            # First visit add to path and color red
            cell.visited = True
            self.path.append(cell.address)
            self.window.animator.draw_frame(cell.address, ("cell", "red"))
        elif has_unv_neighbors > 0:
            # Backtrack to search unvisited neighbors add to path
            self.path.append(cell.address)
        else:
            # Backtrack and no unvisited neighbors remain color pink (searched path)
           self.window.animator.draw_frame(cell.address, ("cell", "pink"))