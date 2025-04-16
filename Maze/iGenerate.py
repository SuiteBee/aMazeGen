from abc import ABC, abstractmethod
from Maze.cell import Cell
#from Draw.plot import Plot
from Draw.kinterPlot import KinterPlot

class IGenerate(ABC):
    def __init__(self, width: int, height: int, isAnimated: bool):
        """isAnimated will introduce a timestep to visualize the generation of the maze
        """
        
        self.width = width
        self.height = height
        self.isAnimated = isAnimated
        
        # Maze resides in cells
        self.cells = [[Cell() for y in range(height)] for x in range(width)]
        self.visited = []
        self.unvisited = [] 
        self.path = []
        
        # Possible Directions (Up), (Down), (Left), (Right)
        # Directions as x,y coordinates
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        
        # The visualized maze (animated will include a pause)
        self.plot = KinterPlot(width, height, isAnimated)
        
    @abstractmethod
    def generate(self) -> list[list[Cell]]:
        """Utilize the algorithm instance create and return a 2d list of Cell with a given width x height
        
        Return 2d list of Cell to represent maze
        """
        pass
    
    def _fill_unvisited(self) -> list[(int,int)]:
        arr = []
        for x in range(self.width):
            for y in range(self.height):
                arr.append((x,y))
        return arr
    
    def _add_cell(self, address: tuple[int,int]) -> None:
        if address not in self.visited:
            self.visited.append(address)
            
        if address in self.unvisited:
            self.unvisited.remove(address)
        
        # Cells added to maze are denoted as white squares    
        self.plot.draw_frame(address, ("cell", "white"))
        
    def _cut_path(self, first, second) -> None:
        
            # Get the direction we came from
            dir = self.__get_direction(first, second)
            
            plot_frames = []

           # Since we are traveling in reverse we can interpret this is as coming from [dir]
            if dir == "down":
                # Remove walls from maze
                self.cells[first[0]][first[1]].top = 0
                self.cells[second[0]][second[1]].bottom = 0
                
                # Remove walls from plot
                plot_frames.append((first, ("border", "top")))
                plot_frames.append((second, ("border", "bottom")))
            elif dir == "up":
                self.cells[first[0]][first[1]].bottom = 0
                self.cells[second[0]][second[1]].top = 0
                
                plot_frames.append((first, ("border", "bottom")))
                plot_frames.append((second, ("border", "top")))
            elif dir == "left":
                self.cells[first[0]][first[1]].right = 0
                self.cells[second[0]][second[1]].left = 0

                plot_frames.append((first, ("border", "right")))
                plot_frames.append((second, ("border", "left")))
            elif dir == "right":
                self.cells[first[0]][first[1]].left = 0
                self.cells[second[0]][second[1]].right = 0
                
                plot_frames.append((first, ("border", "left")))
                plot_frames.append((second, ("border", "right")))
                
            self.plot.draw_multiple(plot_frames)
        
    def __get_direction(self, first: tuple[int,int], second: tuple[int,int]) -> str:       
        direction = first[0] - second[0], first[1] - second[1]
        index = self.directions.index(direction)

        if index == 0:
            return 'up'
        elif index == 1:
            return 'down'
        elif index == 2:
            return 'left'
        elif index == 3:
            return 'right'