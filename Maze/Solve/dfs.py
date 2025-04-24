from Maze.iSolvable import ISolvable
from Maze.cell import Cell
from Draw.tkController import TkController
import random

class DFS(ISolvable):
    def __init__(self, output: TkController, maze: list[list[Cell]]):
        super().__init__(output, maze)
        
    def solve(self, start: tuple[int,int], finish: tuple[int,int]) -> list[Cell]: 
        self.start = start
        self.finish = finish
        
        self.__recursive_depth_search(self._get_cell(start))
        
        while len(self.path) > 0:
            address = self.path.pop(0)
            self.window.animator.queue_frame(address, ("cell", "green"))
            
            cell = self._get_cell(address)
            self.solution.append(cell)
        
        self.window.animator.draw_multiple()
        
        return self.solution
        
    def __recursive_depth_search(self, cell: Cell) -> None:
        
        if cell.address == self.finish:
            self.__visit(cell, False)
            return

        unv_neighbors = [neighbor for neighbor in self._get_neighbors(cell) if not neighbor.visited]
        has_unv_neighbors = len(unv_neighbors) > 0

        self.__visit(cell, has_unv_neighbors)
        
        if has_unv_neighbors:
            next_cell = random.choice(unv_neighbors)
            self.__recursive_depth_search(next_cell)
        else:
            next_address = self.path.pop()
            next_cell = self._get_cell(next_address)
            self.__recursive_depth_search(next_cell)

    def __visit(self, cell: Cell, has_unv_neighbors: bool):
        if not cell.visited:
            cell.visited = True
            self.path.append(cell.address)
            self.window.animator.draw_frame(cell.address, ("cell", "red"))
        elif has_unv_neighbors > 0:
            self.path.append(cell.address)
        else:
           self.window.animator.draw_frame(cell.address, ("cell", "pink"))