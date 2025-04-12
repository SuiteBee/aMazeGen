import matplotlib.pyplot as plt
from Draw.plotCell import PlotCell

class Plot:
    def __init__(self, cells):
        self.cells = cells
        self.width = len(cells)
        self.height = len(cells[0])
        
        self.cellSize = 1
        self.edgewidth = 1.5
        
        # Create a figure and axes
        self.fig, self.ax = plt.subplots(figsize=(10,10))

        self.__format_plot()
        
    def __format_plot(self):
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
        
    def draw(self):
        
        # Set entry and exit (top left, bottom right)
        self.cells[0][self.height - 1].left = 0
        self.cells[self.width - 1][0].right = 0
        
        # Draw entry and exit arrows
        self.ax.arrow(-1, self.height - 0.5, .4, 0, fc="green", ec="green", head_width=0.3, head_length=0.3)
        self.ax.arrow(self.width, 0.5, 0.4, 0, fc="red", ec="red", head_width=0.3, head_length=0.3)
        
        # Fill grid based on cells
        for x in range(self.width):
            for y in range(self.height):
                
                # Get our cell shape, size, color and borders
                plot_cell = PlotCell(self.cells[x][y], x, y, self.cellSize, self.edgewidth)

                # Draw our cell
                self.ax.add_patch(plot_cell.patch)
                
                # Draw borders
                self.ax.add_collection(plot_cell.borders)
                                
        # Display plot
        plt.show()
            
    def live_plot(self):
        
         # Set entry and exit (top left, bottom right)
        self.cells[0][self.height - 1].left = 0
        self.cells[self.width - 1][0].right = 0
        
        # Draw entry and exit arrows
        self.ax.arrow(-1, self.height - 0.5, .4, 0, fc="green", ec="green", head_width=0.3, head_length=0.3)
        self.ax.arrow(self.width, 0.5, 0.4, 0, fc="red", ec="red", head_width=0.3, head_length=0.3)
        
        # Fill grid with empty cells
        for x in range(self.width):
            for y in range(self.height):
                color = "black"
                if self.cells[x][y].visited:
                    color = "white"
                
                # Get our cell shape and borders
                plot_cell = PlotCell(self.cells[x][y], x, y, color, self.cellSize, self.edgewidth)

                # Draw our cell
                self.ax.add_patch(plot_cell.patch)
                
                # Do not add borders yet
        
            
    def draw_single(self, cell, x, y, facecolor):
        # Get our cell shape and borders
        plot_cell = PlotCell(cell, x, y, facecolor, self.cellSize, self.edgewidth)
        
        # Draw our cell
        self.ax.add_patch(plot_cell.patch)
                
        plt.pause(0.05)
        
    def draw_single_border(self, cell, x, y):
        # Get our cell shape, size, color and borders
        plot_cell = PlotCell(cell, x, y, "none", self.cellSize, self.edgewidth)
        
        # Erase existing borders
        self.ax.add_collection(plot_cell.eraseBorders)
        
        # Draw our border now
        self.ax.add_collection(plot_cell.borders)
        
    def show(self):
        plt.show()
        
    
    
    