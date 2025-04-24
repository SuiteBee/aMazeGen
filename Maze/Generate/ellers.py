from Maze.iGenerable import IGenerable
from Maze.cell import Cell
from Draw.tkController import TkController
import random

class Ellers(IGenerable):
    def __init__(self, output: TkController, width, height):
        super().__init__(output, width, height)

        # For Ellers we need to keep track of a list of disjointed sets
        # We will keep the length at most the width of the maze
        self.set_paths = []

    def generate(self) -> list[list[Cell]]:

        # Starting from the top until the second to last row
        for row_index in range(self.height - 1, 0, -1):
            
            # Get a row of cells and create a new path or continue a path from above
            current_row = self.__get_cell_row(row_index)    
            self.__expand_path(current_row)
            
            # Randomly remove vertical walls and join the opposing sets
            # Adjacent cells belonging to the same set will not have walls removed
            self.__remove_walls(current_row, False)
            
            # Randomly remove horizontal floors from our current sets
            # We will maintain that every set has at least one downward path
            self.__remove_floors()
            
            # Any cells that kept their horizontal floor can be removed from their sets
            self.__clean_path(current_row)
            
        # Last row will not remove vertical walls randomly
        # This time combine disjointed sets until set_paths is one singular set
        last_row = self.__get_cell_row(0)
        self.__expand_path(last_row)
        self.__remove_walls(last_row, True)

        return self.cells
    
    def __get_cell_row(self, index) -> list[Cell]:
        """Get a row of cells (0 is bottom) and color them white
        """
        row = []
        for column in range(self.width):
            cell = self.cells[column][index]
            row.append(cell)  
        return row
    
    def __get_path(self, cell: Cell) -> list[tuple[int,int]]:
        """Loop through sets until we find one that contains our cell address
        """
        for path in self.set_paths:
            if cell.address in path:
                return path
            
    def __expand_path(self, row: list[Cell]) -> None:
        """Get our working row of disjointed sets
        """
        for cell in row:
            if cell.top == 0:
                # If this cell does not have a ceiling we can add it to the set the cell above was a member of
                cell_above = self.cells[cell.x][cell.y+1]
                existing_path = self.__get_path(cell_above)
                
                # We no longer need the old cell in the set to keep track of its path so remove it
                self.__swap_path(existing_path, cell, cell_above)
            else:
                # This is considered a new path because it does not connect to any cells so we can add it to its own set
                # Can be merged with another set in later step
                new_path = [cell.address]
                self.set_paths.append(new_path)
                self.window.animator.draw_frame(cell.address, ("cell", "red"))
            
    def __clean_path(self, row: list[Cell]) -> None:
        """Remove cells from paths that can no longer expand downwards
        """
        for cell in row:
            if cell.bottom == 1:
                # If this cell has a floor we can remove it from its set
                # The path was terminated here or we can follow it by the remaining member cells that did travel downwards 
                existing_path = self.__get_path(cell)
                existing_path.remove(cell.address)
            
            self.window.animator.queue_frame(cell.address, ("cell", "white"))
            
        self.window.animator.draw_multiple()
            
    def __swap_path(self, path: list[tuple[int,int]], toAdd: Cell, toRemove: Cell) -> None:
        """Remove redundant address from given path by replacing it with a relavent one 
        """
        # This set has traveled downwards at the toRemove cell
        # We can track this path by removing the above cell and adding the one below
        path.remove(toRemove.address)
        path.append(toAdd.address)
        
        self.window.animator.queue_frame(toAdd.address, ("cell", "pink"))
        self.window.animator.queue_frame(toRemove.address, ("cell", "white"))
        self.window.animator.draw_multiple()
        
        
    def __merge_path(self, first: list[tuple[int,int]], second: list[tuple[int,int]]) -> None:
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
            self.window.animator.queue_frame((address[0], address[1]), ("cell", "white"))
            
        self.window.animator.draw_multiple()
        
    def __has_exit_path(self, path: list[tuple[int,int]]) -> bool:
        """Check all cells in the set(path) to ensure at minimum one of them has a downward exit
        """
        for address in path:
            if self._get_cell(address).bottom == 0:
                return True
            
        return False
   
    def __remove_walls(self, row: list[Cell], final_row: bool) -> None:
        """From left to right of row, randomly decide to remove vertical walls separating cells that are not a part of the same path
        
        When a wall is removed we will join the two paths on the opposing sides of the removed wall
        """
        for index, cell in enumerate(row[:-1]):
            # Get the set this cell is a member of
            path = self.__get_path(cell)
            neighbor = row[index+1]
            
            # If the neighboring cell is not in the same set we can continue
            if not neighbor.address in path:
                # We are not on the last row, flip a coin to remove the wall
                if self.__destroy_wall(cell, not final_row):
                    # The wall was removed, join the sets on either side
                    neighbor_path = self.__get_path(neighbor)
                    self.__merge_path(path, neighbor_path)
                    
    def __destroy_wall(self, cell: Cell, rng: bool) -> bool:
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
            
            self.window.animator.queue_frame(cell.address, ("border", "right"))
            self.window.animator.queue_frame(neighbor.address, ("border", "left"))

        return remove_right
                 
    def __remove_floors(self) -> None: 
        """For every cell address in row (indiscriminant order), randomly remove horizontal walls
        
        Will loop through set paths and ensure at least one cell in every set has a downward exit
        """
        # For every set
        for path in self.set_paths:
            # Randomly remove a horizontal floor from each cell address
            for address in path:
                self.__destory_floor(self._get_cell(address), True)

            # If we didn't remove one from the above set(path) pick one at random from the set to remove
            if not self.__has_exit_path(path):
                random_address = random.choice(path)
                self.__destory_floor(self._get_cell(random_address), False)
        
        # Clear out frame_queue (draw removed floors)                
        self.window.animator.draw_multiple()

    def __destory_floor(self, cell: Cell, rng: bool) -> bool:               
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
        
            self.window.animator.queue_frame(cell.address, ("border", "bottom"))
            self.window.animator.queue_frame(neighbor.address, ("border", "top"))

        return remove_bottom
        
        