from Maze.iSolvable import ISolvable
from Maze.cell import Cell
from Draw.tkDraw import TkDraw
import random

class DFS(ISolvable):
    def __init__(self, output: TkDraw, maze: list[list[Cell]]):
        super().__init__(output, maze)
        
    def solve(self, start: tuple[int,int], finish: tuple[int,int]) -> list[Cell]: 
        self.start = start
        self.finish = finish
        
        self.__recursive_depth_search(self._get_cell(start))
        
        while len(self.path) > 0:
            address = self.path.pop(0)
            self.window.queue_frame(address, ("cell", "green"))
            
            cell = self._get_cell(address)
            self.solution.append(cell)
        
        self.window.draw_multiple()
        
        return self.solution
        
    def __recursive_depth_search(self, cell: Cell) -> None:
        
        if cell.address == self.finish:
            self.__visit(cell, False)
            return

        unv_neighbors = [neighbor for neighbor in self.__get_neighbors(cell) if not neighbor.visited]
        has_unv_neighbors = len(unv_neighbors) > 0

        self.__visit(cell, has_unv_neighbors)
        
        if has_unv_neighbors:
            next_cell = random.choice(unv_neighbors)
            self.__recursive_depth_search(next_cell)
        else:
            next_address = self.path.pop()
            next_cell = self._get_cell(next_address)
            self.__recursive_depth_search(next_cell)

    def __get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors = []
        
        if cell.left == 0 and not cell.address == self.start:
            neighbors.append(self._get_left(cell.address))
            
        if cell.right == 0 and not cell.address == self.finish:
            neighbors.append(self._get_right(cell.address))
            
        if cell.top == 0:
            neighbors.append(self._get_above(cell.address))
            
        if cell.bottom == 0:
            neighbors.append(self._get_below(cell.address))
            
        return neighbors
            
    def __visit(self, cell: Cell, has_unv_neighbors: bool):
        if not cell.visited:
            cell.visited = True
            self.path.append(cell.address)
            self.window.draw_frame(cell.address, ("cell", "red"))
        elif has_unv_neighbors > 0:
            self.path.append(cell.address)
        else:
            self.window.draw_frame(cell.address, ("cell", "pink"))