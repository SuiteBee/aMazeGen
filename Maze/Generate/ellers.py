from Maze.iGenerate import IGenerate
from Maze.cell import Cell
import random

class Ellers(IGenerate):
    def __init__(self, width, height, isAnimated):
        super().__init__(width, height, isAnimated)

        # For Ellers we need to keep track of a list of disjointed sets
        # We will keep the length at most the width of the maze
        self.set_paths = []

    def generate(self) -> list[list[Cell]]:
        
        # Starting from the top until the second to last row
        for row_index in range(self.height - 1, 0, -1):
            
            # Get a row of cells and create a new path or continue a path from above
            current_row = self.get_cell_row(row_index)    
            self.expand_path(current_row)
            
            # Randomly remove vertical walls and join the opposing sets
            # Adjacent cells belonging to the same set will not have walls removed
            self.remove_walls(current_row, False)
            
            # Randomly remove horizontal floors from our current sets
            # We will maintain that every set has at least one downward path
            self.remove_floors()
            
            # Any cells that kept their horizontal floor can be removed from their sets
            self.clean_path(current_row)
            
        # Last row will not remove vertical walls randomly
        # This time combine disjointed sets until set_paths is one singular set
        last_row = self.get_cell_row(0)
        self.expand_path(last_row)
        self.remove_walls(last_row, True)
                  
        # Tell our drawing library we have finished generating 
        self.window.finish_generation()
        
        return self.cells
    
    def get_cell_row(self, index) -> list[Cell]:
        """Get a row of cells (0 is bottom) and color them white
        """
        row = []
        for column in range(self.width):
            cell = self.cells[column][index]
            row.append(cell)  
        return row
    
    def get_path(self, cell: Cell) -> list[tuple[int,int]]:
        """Loop through sets until we find one that contains our cell address
        """
        for path in self.set_paths:
            if (cell.x, cell.y) in path:
                return path
            
    def expand_path(self, row: list[Cell]) -> None:
        """Get our working row of disjointed sets
        """
        for cell in row:
            if cell.top == 0:
                # If this cell does not have a ceiling we can add it to the set the cell above was a member of
                cell_above = self.cells[cell.x][cell.y+1]
                existing_path = self.get_path(cell_above)
                
                # We no longer need the old cell in the set to keep track of its path so remove it
                self.path_swap(existing_path, cell, cell_above)
            else:
                # This is considered a new path because it does not connect to any cells so we can add it to its own set
                # Can be merged with another set in later step
                new_path = [(cell.x, cell.y)]
                self.set_paths.append(new_path)
                self.window.draw_frame((cell.x, cell.y), ("cell", "red"))
            
    def clean_path(self, row: list[Cell]) -> None:
        """Remove cells from paths that can no longer expand downwards
        """
        for cell in row:
            if cell.bottom == 1:
                # If this cell has a floor we can remove it from its set
                # The path was terminated here or we can follow it by the remaining member cells that did travel downwards 
                existing_path = self.get_path(cell)
                existing_path.remove((cell.x, cell.y))
            
            self.window.queue_frame((cell.x, cell.y), ("cell", "white"))
            
        self.window.draw_multiple()
            
    def path_swap(self, path: list[tuple[int,int]], toAdd: Cell, toRemove: Cell) -> None:
        """Remove redundant address from given path by replacing it with a relavent one 
        """
        # This set has traveled downwards at the toRemove cell
        # We can track this path by removing the above cell and adding the one below
        address_to_remove = (toRemove.x, toRemove.y)
        path.remove(address_to_remove)
        path.append((toAdd.x, toAdd.y))
        
        self.window.queue_frame((toAdd.x, toAdd.y), ("cell", "pink"))
        self.window.queue_frame((toRemove.x, toRemove.y), ("cell", "white"))
        self.window.draw_multiple()
        
        
    def path_merge(self, first: list[tuple[int,int]], second: list[tuple[int,int]]) -> None:
        """A vertical wall was removed and the paths on either side will be joined into one set
        """
        combined = first + second
        
        # Get index of the first set and join with the second
        path_index = self.set_paths.index(first)
        self.set_paths[path_index] = combined
        
        # Remove the second set
        self.set_paths.remove(second)   
        
        for address in combined:
            # The following is queued to color cell and remove borders at the same time
            self.window.queue_frame((address[0], address[1]), ("cell", "white"))
            
        self.window.draw_multiple()
   
    def remove_walls(self, row: list[Cell], final_row: bool) -> None:
        """From left to right of row, randomly decide to remove vertical walls separating cells that are not a part of the same path
        
        When a wall is removed we will join the two paths on the opposing sides of the removed wall
        """
        for index, cell in enumerate(row[:-1]):
            # Get the set this cell is a member of
            path = self.get_path(cell)
            neighbor = row[index+1]
            
            # If the neighboring cell is not in the same set we can continue
            if not (neighbor.x, neighbor.y) in path:
                # We are not on the last row, flip a coin to remove the wall
                if self.destroy_wall(cell, not final_row):
                    # The wall was removed, join the sets on either side
                    neighbor_path = self.get_path(neighbor)
                    self.path_merge(path, neighbor_path)
                 
    def remove_floors(self) -> None: 
        """For every cell address in row (indiscriminant order), randomly remove horizontal walls
        
        Will loop through set paths and ensure at least one cell in every set has a downward exit
        """
        # For every set
        for path in self.set_paths:
            # Randomly remove a horizontal floor from each cell address
            for address in path:
                cell = self.cells[address[0]][address[1]]
                self.destory_floor(cell, True)

            # If we didn't remove one from the above set(path) pick one at random from the set to remove
            if not self.set_has_exit(path):
                random_address = random.choice(path)
                random_cell = self.cells[random_address[0]][random_address[1]]
                self.destory_floor(random_cell, False)
        
        # Clear out frame_queue (draw removed floors)                
        self.window.draw_multiple()

    def set_has_exit(self, path: list[tuple[int,int]]) -> bool:
        """Check all cells in the set(path) to ensure at minimum one of them has a downward exit
        """
        for address in path:
            if self.cells[address[0]][address[1]].bottom == 0:
                return True
            
        return False

    def destroy_wall(self, cell: Cell, rng: bool) -> bool:
        """Remove right cell border, randomly if rng=True and return if successful
        
        Set cell borders and draw to screen
        """
        # Randomly decide to remove wall
        remove_right = random.choice([True, False]) if rng else True

        if remove_right:
            # Neighbor is cell to the right
            neighbor: Cell = self.cells[cell.x+1][cell.y]
            
            cell.right = 0
            neighbor.left = 0
            
            self.window.queue_frame((cell.x, cell.y), ("border", "right"))
            self.window.queue_frame((neighbor.x, neighbor.y), ("border", "left"))

        return remove_right
            

    def destory_floor(self, cell: Cell, rng: bool) -> bool:               
        """Remove bottom cell border, randomly if rng=True and return if successful
        
        Set cell borders and draw to screen
        """
        # Randomly decide to remove floor
        remove_bottom = random.choice([True, False]) if rng else True
        
        if remove_bottom:
            # Neighbor is cell below
            neighbor: Cell = self.cells[cell.x][cell.y-1]
            
            cell.bottom = 0
            neighbor.top = 0
        
            self.window.queue_frame((cell.x, cell.y), ("border", "bottom"))
            self.window.queue_frame((neighbor.x, neighbor.y), ("border", "top"))

        return remove_bottom
        
        