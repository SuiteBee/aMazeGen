from Maze.iGenerate import IGenerate
from Maze.cell import Cell
import random

class Ellers(IGenerate):
    def __init__(self, width, height, isAnimated):
        super().__init__(width, height, isAnimated)
        
        # For Ellers unvisited is initialized with all cells
        self.unvisited = self._fill_unvisited()
        self.unique_sets = []
        
    def generate(self) -> list[list[Cell]]:

        for i in range(1,int(self.width/2)):
            self.process_row([row[self.width-i] for row in self.cells])
            
        # Tell our drawing library we have finished generating 
        self.window.finish_generation()
        
        return self.cells
        
    def process_row(self, row: list[Cell]):
        # Add each cell to its own set
        for cell in row:
            self.unique_sets.append([cell])

        self.process_right(row)
        self.process_down()
   
    def process_right(self, row: list[Cell]):
        new_unique_sets = []
        
        # For every cell in row except last randomly remove right walls
        for i, cell in enumerate(row):
            
            self.window.draw_frame((cell.x, cell.y), ("cell", "white"))
            
            if i < len(row) - 1:
                # Leave wall in place if next neighbor is in our own set
                if not self.neighbor_in_set(cell):
                    new_set = self.rng_remove_right(i, cell)
                    new_unique_sets.append(new_set)

        self.unique_sets = new_unique_sets
                    
    def process_down(self):
         # For every unique set
        for group in self.unique_sets:
            # Remove bottom if cell is in a set on its own
            if len(group) == 1:
                group[0].bottom = 0
                self.window.draw_frame((group[0].x, group[0].y), ("border", "bottom"))
                self.window.draw_frame((group[0].x, group[0].y-1), ("border", "top"))
            else:
                self.rng_remove_bottom(group)
                

    def neighbor_in_set(self, cell: Cell):
        """Find the unique set containing our cell and see if the neighbor to the right is also there
        """
        for group in self.unique_sets:
            if cell in group:
                # Check neighbor
                return self.cells[cell.x + 1][cell.y] in group
    
    def only_cell_in_set(self, cell: Cell):
        """Find the unique set containing our cell and see if it is the only one"""
        for group in self.unique_sets:
            if cell in group:
                # Check neighbor
                return len(group) == 1
            
    def set_has_exit(self, group: list[Cell]):
        for cell in group:
            if cell.bottom == 0:
                return True
                            
        return False
            
    def rng_remove_right(self, set_index: int, cell: Cell):
        # Randomly decide to remove wall
        remove_right_wall = random.choice([True, False])
        if remove_right_wall:
            cell.right = 0
            self.window.draw_frame((cell.x, cell.y), ("border", "right"))
            self.window.draw_frame((cell.x+1, cell.y), ("border", "left"))
            
            
            # Join sets when removed
            return self.unique_sets[set_index] + self.unique_sets[set_index+1]
        
        return self.unique_sets[set_index]
        
    def rng_remove_bottom(self, group: list[Cell]):
        for cell in group:                  
            # Randomly decide to remove wall
            remove_bottom_wall = random.choice([True, False])
            if remove_bottom_wall:
                cell.bottom = 0
                self.window.draw_frame((cell.x, cell.y), ("border", "bottom"))
                self.window.draw_frame((cell.x, cell.y-1), ("border", "top"))
                
        # Ensure unique set has an exit
        if not self.set_has_exit(group):
            random_cell = random.choice(group)
            random_cell.bottom = 0
            self.window.draw_frame((random_cell.x, random_cell.y), ("border", "bottom"))
            self.window.draw_frame((random_cell.x, random_cell.y-1), ("border", "top"))
        

        
        
