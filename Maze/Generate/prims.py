from Maze.iGenerate import IGenerate
from Maze.cell import Cell
from Draw.tkDraw import TkDraw
import random

class Prims(IGenerate):
    def __init__(self, output: TkDraw, width, height, isAnimated):
        super().__init__(output, width, height, isAnimated)
        
        # For prims unvisited is empty until we select our starting cell
        # We refer to this as the frontier i.e. all cells NOT in the maze neighboring cells that ARE within the maze
        self.unvisited = []
        
    def generate(self) -> list[list[Cell]]:
        # Add first point to the maze
        start = (random.randrange(self.width - 1), random.randrange(self.height - 1))
        self._add_cell(start)
        self.__expand_frontier(start)
        
        # Loop until all frontier cells are visited
        while len(self.unvisited) > 0:     
            # Choose next random point from frontier
            frt = random.choice(self.unvisited)
            
            # Cut a path back to maze (borders)
            cell_in_maze = self.__get_visited_neighbor(frt)
            self._cut_path(frt, cell_in_maze)
            
            # Add our next frontier cell to maze
            self._add_cell(frt)
            
            self.__expand_frontier(frt)
        
        return self.cells
        
    def __expand_frontier(self, address: tuple[int,int]) -> None:
        new_frontier = self.__get_neighbors(address)

        for cell in new_frontier:
            # Cell is not already a part of the maze or frontier
            if not cell in self.visited and not cell in self.unvisited:
                self.unvisited.append(cell)
            
                # Cells within the frontier are denoted as red squares
                self.window.queue_frame(cell, ("cell", "red"))
        
        # Draw all of our expanded frontier cells at once
        self.window.draw_multiple()
        
    def __get_neighbors(self, address: tuple[int,int]) -> list[tuple[int,int]]:
        """Return a list of neighboring cell coordinates that are within the maze bounds
        """
        
        neighbors = []
        
        # For every possible direction from address
        for direction in self.directions:
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