from Maze.iSolvable import ISolvable
from Maze.cell import Cell
from Draw.tkController import TkController

class BFS(ISolvable):
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
        self.solution = self.__get_shortest_path(first_cell, last_cell)
        
        return self.solution
    
    def __get_shortest_path(self, first_cell: Cell, last_cell: Cell) -> list[Cell]:
        """Color and return a chain of cells from first to last connected by Cell.parent property
        """
        
        shortest_path = []
        while last_cell.address != first_cell.address:
            # Add our last cell to the path and color it green
            shortest_path.insert(0, last_cell)
            self.window.animator.queue_frame(last_cell.address, ("cell", "green"))

            # Set our last cell to be its parent (where it came from)
            last_cell = self._get_cell(last_cell.parent)
            
        self.window.animator.queue_frame(first_cell.address, ("cell", "green"))
        self.window.animator.draw_pending()
        
        return shortest_path
    
    def __expand_search(self, cell: Cell) -> None:
        """Visit all unvisited neighbors of cell and record cell as their parent
        """
        unv_neighbors = [neighbor for neighbor in self._get_neighbors(cell) if not neighbor.visited]
        has_unv_neighbors = len(unv_neighbors) > 0

        if has_unv_neighbors:
            for unv in unv_neighbors:
                self.__visit(unv, cell)
                
                # Color our cell red to denote it is the next cell to be examined
                self.window.animator.queue_frame(unv.address, ("cell", "red"))
                
        # Color our examined cell pink as it is no longer at the forefront of the search
        self.window.animator.queue_frame(cell.address, ("cell", "pink"))
                    

    def __visit(self, cell: Cell, origin: Cell):
        """Visit cell and set parent(origin)
        """
        cell.visited = True
        cell.parent = origin.address
        self.path.insert(0, cell.address)