from Maze.iSolvable import ISolvable
from Maze.cell import Cell
from Draw.tkController import TkController

class Best(ISolvable):
    def __init__(self, output: TkController, maze: list[list[Cell]]):
        super().__init__(output, maze)
        
    def solve(self, start: tuple[int,int], finish: tuple[int,int]) -> list[Cell]: 
        self.start_address = start
        self.finish_address = finish
        
        # Begin search from starting cell
        current_cell = self._get_cell(self.start_address)
        
        # Visit the closest cell to the exit from our path until we reach the exit
        while current_cell.address != self.finish_address:
            # Visit this cell
            self.__visit(current_cell)

            # Get the next closest cell
            next_cell = self._get_next()   
            
            # Color old cells pink
            self.window.animator.draw_frame(current_cell.address, ("cell", "pink"))
            
            # Set our next cell to current
            current_cell = next_cell

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
    
    def _get_next(self) -> Cell:
        """Choose the next cell based on the distance from visited cell unvisited neighbors -> exit
        """
        remove_from_path = []
        closest_cell = None
        current_dst = None
        
        for address in self.path:
            path_cell = self._get_cell(address)
            unv_neighbor = self.__closest_neighbor(path_cell)
            
            if unv_neighbor is None:
                # Cell has no unvisited neighbors remove from path
                remove_from_path.append(address)
            else:
                # Set parent of neighbor so we can follow path back for solution
                unv_neighbor.parent = path_cell.address
                
                # Cell has unvisited neighbors check to see if one of them is closer   
                if current_dst is None or unv_neighbor.distance < current_dst:
                    closest_cell = unv_neighbor
                    current_dst = unv_neighbor.distance
                   
        # Remove cells with no remaining unvisited neighbors from path
        for address in remove_from_path or []:
            self.path.remove(address)
                    
        return closest_cell
    
    def __closest_neighbor(self, cell: Cell) -> Cell:
        """Return the closest unvisited neighbor to cell
        """
        
        closest_cell = None
        current_dst = None
        
        # Get list of unvisited neighbors
        unv_neighbors = [neighbor for neighbor in self._get_neighbors(cell) if not neighbor.visited]
        
        # Calculate distance of each unvisited neighbor and store the closest
        for neighbor in unv_neighbors or []:
            dst = self.__calculate_distance(neighbor)
            if current_dst is None or dst < current_dst:
                closest_cell = neighbor
                current_dst = neighbor.distance
                
        return closest_cell
    
    def __calculate_distance(self, cell: Cell) -> int:
        """Set and return the Manhattan distance between cell and the exit
        """
        if cell.distance is None:
            cell.distance = abs(cell.x - self.finish_address[0]) + abs(cell.y - self.finish_address[1])
        
        return cell.distance
    
    def __visit(self, cell: Cell):
        """Mark cell as visited and append to path
        """
        # First visit, color cell red and add to path
        cell.visited = True
        self.path.append(cell.address)
        self.window.animator.draw_frame(cell.address, ("cell", "red"))
        
        # Get all unvisited neighbors of cell
        unv_neighbors = [neighbor for neighbor in self._get_neighbors(cell) if not neighbor.visited]
        
        # Color neighbors yellow
        for neighbor in unv_neighbors or []:
            self.window.animator.queue_frame(neighbor.address, ("cell", "yellow"))
        
        self.window.animator.draw_pending()