import random

from Maze.iGenerable import IGenerable
from Maze.cell import Cell
from Utility.enums import Instruction
from Utility.enums import Color
from Interface.GUI.tkController import TkController

class Wilsons(IGenerable):
    """Implementation of Wilsons's maze generation algorithm
    
    Builds a maze by taking random walks from arbitrary cells back to cells in the maze
    """
    
    def __init__(self, output: TkController, width, height):
        super().__init__(output, width, height)
        
        # For wilsons unvisited is initialized with all cells
        self.unvisited = self._fill_unvisited()
        self.path = []
        
    def generate(self) -> list[list[Cell]]:
        # Add first point to the maze
        start = (random.randrange(self.width - 1), random.randrange(self.height - 1))
        self._add_cell(start)
        
        # Loop until all cells are visited
        while len(self.unvisited) > 0:     
            # Choose next random point
            src = random.choice(self.unvisited)
            
            # Walk back to a point in the maze
            self.__take_walk(src)
            
            # Mark all cells in our path as visited (i.e. add to maze)
            for i in range(len(self.path)):
                step = self.path[i]
                self._add_cell(step)
            
            # Walk our path in reverse (set borders)
            self.__walk_back()
            
            # Clear out the frame queue (walls)
            self.window.animator.draw_pending()

        return self.cells
    
    def name(self) -> str:
        return "Wilson's"

    # Walk from random point to point in maze
    def __take_walk(self, src: tuple[int,int]) -> None:
        """Randomly move in any direction from src coordinates until we hit a point in the maze
        
        If we run into this path we back track until that point and continue
        """
        
        # Add our start to the path
        self.path.append(src)
        
        # Mark our travel path red
        self.window.animator.draw_frame(src, Instruction.CELL, Color.RED)
        
        # Get next cell to add to path
        current = self.__take_step(src)

        # Continue until we have reached the random point
        while current not in self.visited:
            # Loop Detected
            if current in self.path:
                # Remove loop from path and retry
                while current != self.path[-1]:
                    removed = self.path.pop()
                    
                    # Restore our backtracked cells to the original black color
                    self.window.animator.draw_frame(removed, Instruction.CELL, Color.BLACK)
            else:
                # Path is valid continue from current
                self.path.append(current)
                
                # Mark our travel path red
                self.window.animator.draw_frame(current, Instruction.CELL, Color.RED)
                
            # Get next cell to add to path
            current = self.__take_step(current)
            
        # Add our target to process wall removal
        self.path.append(current)
        
    def __take_step(self, src: tuple[int,int]) -> tuple[int,int]:
        """Pick a random direction to walk in, if the coordinates are within maze bounds return those coordinates
        
        Call is recursive until we find a valid direction to go
        """
        
        travel = random.choice(self.dir_coords)
        
        nextCellX = src[0] + travel[0]
        nextCellY = src[1] + travel[1]
        
        # Check if the next cell x,y coordinates are within the maze
        if(nextCellX >= 0 and nextCellX < self.width and nextCellY >= 0 and nextCellY < self.height):
            return (nextCellX, nextCellY)
        else:
            return self.__take_step(src)
    
    def __walk_back(self) -> None:
        """For each cell in our random walk, cut a path between each in reverse
        """
        
        tail = self.path.pop()
        
        while len(self.path) > 0:
            previous = self.path.pop()
            
            # Set walls relative to path taken in reverse
            # i.e. open wall in path of travel
            self._cut_path(tail, previous)
        
            # Set tail to be the cell we just processed for next iteration
            if len(self.path) > 0:
                tail = previous