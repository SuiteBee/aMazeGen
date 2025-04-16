from matplotlib import pyplot as plt
from Maze.cell import Cell
from Draw.mplCell import MplCell

class MplPlot:
    def __init__(self, width, height, isAnimated):
        self.isAnimated = isAnimated 
        self.timeStep = 0.01
        
        self.width = width
        self.height = height

        self.cellSize = 1
        self.edgewidth = 1.5
        
        # Init representation of our maze with plot cells (visualized)
        self.graph = self.__get_graph()
        
        # Create a figure and axes
        self.fig = plt.figure(figsize=(10,10))
        self.ax = self.fig.add_subplot()
        
        self.__configure_plot()
                
    def draw_start(self) -> None:
        """Fill grid with empty cells and walls enabled
        """
        
        for x in range(self.width):
            for y in range(self.height):
                # Get our cell shape and borders
                plot_cell = self.graph[x][y]

                # Draw our cell
                self.ax.add_patch(plot_cell.patch)
                
                # Draw borders
                self.ax.add_collection(plot_cell.borders)
        
    def draw_end(self) -> None:
        """Draw entry/exit and arrows then show plot
        """
        
        # Set entry and exit (top left, bottom right)
        self.set_border(0, self.height - 1, "left", False)
        self.set_border(self.width - 1, 0, "right", False)
        
        # Draw entry and exit arrows
        self.ax.arrow(-1, self.height - 0.5, .4, 0, fc="green", ec="green", head_width=0.3, head_length=0.3)
        self.ax.arrow(self.width, 0.5, 0.4, 0, fc="red", ec="red", head_width=0.3, head_length=0.3)
        
        plt.show()

    def set_color(self, x: int, y: int, color: str) -> None:
        """Change cell color and pause for timeStep if isAnimated
        """
        
        self.graph[x][y].set_patch_color(color)
        
        if self.isAnimated: 
            plt.pause(self.timeStep)
        
    def set_border_cell(self, cell: Cell, x: int, y: int) -> None:
        """Set all borders based on Cell at x,y
        """
        
        # Bottom
        self.graph[x][y].set_border_active(0, cell.bottom == 1)
        
        # Top 
        self.graph[x][y].set_border_active(1, cell.top == 1)
        
        # Left 
        self.graph[x][y].set_border_active(2, cell.left == 1)
            
        # Right
        self.graph[x][y].set_border_active(3, cell.right == 1)
        
    def set_border(self, x: int, y: int, direction: str, active: bool) -> None:
        """Set single border at x,y at specified direction

        Args:
            direction (str): bottom, top, left, right
            active (bool): Wall enabled
        """
        
        self.graph[x][y].set_border(direction, active)
    
    def __get_graph(self) -> list[list[PlotCell]]:
        """Create a 2d list representation of our maze with PlotCells
        """
        
        graph = [[0 for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                graph[x][y] = PlotCell(x,y, "black", self.cellSize, self.edgewidth)
        
        return graph
        
    def __configure_plot(self) -> None:
        """Set aspect, viewport size and show/hide what we want to see in graph
        """

        # Set aspect ratio to keep cells square
        self.ax.set_aspect("equal")
        
        # Set the border color to white
        self.fig.patch.set_edgecolor("white")
        self.fig.patch.set_linewidth(0)
        
        # Hide axis ticks
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Hide axes
        self.ax.spines[["right", "top", "bottom", "left"]].set_visible(False)

        # Set viewport with padding to allow for uniform borders
        plt.xlim(-1, self.width + 1)
        plt.ylim(-1, self.height + 1)
    