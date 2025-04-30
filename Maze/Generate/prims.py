import random

from Maze.iGenerable import IGenerable
from Utility.enums import Instruction
from Utility.enums import Color
from Maze.cell import Cell
from Interface.GUI.tkController import TkController

class Prims(IGenerable):
    """Implementation of Prim's maze generation algorithm
    
    Starts at a single point and randomly expands to unvisited neighbor cells (frontier) until all cells are visited
    """
    
    def __init__(self, output: TkController, width, height):
        super().__init__(output, width, height)
        
        # For prims unvisited is empty until we select our starting cell
        # We refer to this as the frontier i.e. all cells NOT in the maze neighboring cells that ARE within the maze
        self.unvisited = []
        
    def generate(self) -> list[list[Cell]]:
        # Add first point to the maze
        start = (random.randrange(self.width - 1), random.randrange(self.height - 1))
        self._add_cell(start)
        self.__expand_frontier(start)
        self.window.animator.draw_pending()
        
        # Loop until all frontier cells are visited
        while len(self.unvisited) > 0:     
            # Choose next random point from frontier
            frt = random.choice(self.unvisited)
            
            # Cut a path back to maze (borders)
            cell_in_maze = self.__get_visited_neighbor(frt)
            self._cut_path(frt, cell_in_maze)
            
            # Add our next frontier cell to maze
            self._add_cell(frt)
            
            # Expand frontier from new cell
            self.__expand_frontier(frt)
            
            # Clear out frame queue (frontier cells and walls)
            self.window.animator.draw_pending()
        
        return self.cells
    
    def name(self) -> str:
        return "Prim's"
        
    def __expand_frontier(self, address: tuple[int,int]) -> None:
        new_frontier = self.__get_neighbors(address)

        for cell in new_frontier:
            # Cell is not already a part of the maze or frontier
            if not cell in self.visited and not cell in self.unvisited:
                self.unvisited.append(cell)
            
                # Cells within the frontier are denoted as red squares
                self.window.animator.queue_frame(cell, Instruction.CELL, Color.RED)
        
    def __get_neighbors(self, address: tuple[int,int]) -> list[tuple[int,int]]:
        """Return a list of neighboring cell coordinates that are within the maze bounds
        """
        
        neighbors = []
        
        # For every possible direction from address
        for direction in self.dir_coords:
            neighborX = address[0] + direction[0]
            neighborY = address[1] + direction[1]
            
            # Add cell coordinates that are within the maze bounds
            if neighborX >= 0 and neighborX < self.width and neighborY >= 0 and neighborY < self.height:
                neighbors.append((neighborX, neighborY))
                
        return neighbors
    
    def __get_visited_neighbor(self, address: tuple[int,int]) -> tuple[int,int]:
        """Return random neighboring cell that is part of the maze
        """
             
        # Get neighbors of cell at address
        neighbors = self.__get_neighbors(address)
        
        neighbors_in_maze = []
        for cell in neighbors:
            # Valid cells are in maze
            if cell in self.visited:
                neighbors_in_maze.append(cell)
                
        # Pick a valid cell at random
        return random.choice(neighbors_in_maze)