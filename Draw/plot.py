import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as collect

class Plot:
    def __init__(self, cells):
        self.cells = cells
        self.width = len(cells)
        self.height = len(cells[0])
        
        self.edgewidth = 1.5
        self.cellSize = 1
        self.gridStart = (0,0) 
        
    def draw_grid(self):
        # Create a figure and axes
        fig, ax = plt.subplots(figsize=(10,10))
        
        # Set aspect ration to keep cells square
        ax.set_aspect("equal")
        
        # Set the border color to white
        fig.patch.set_edgecolor('white')
        fig.patch.set_linewidth(0)
        
        # Hide axis ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Show inner border (maze outer walls)
        ax.set_frame_on(True)
        plt.setp(ax.spines.values(), linewidth=self.edgewidth)
        
        # Set Viewport
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)

        # Fill grid based on cells
        for x in range(self.width):
            for y in range(self.height):
                # Retrive cell shape, size and color
                patch = self.get_cell(self.cells[x][y], x, y)
                
                # Get collection of border lines for cell
                borders = self.get_border(self.cells[x][y], patch)
                borderLines = collect.LineCollection(borders, edgecolors="black", linewidths=self.edgewidth)
                
                # Add patch to axis
                ax.add_patch(patch)
                
                # Add borders
                ax.add_collection(borderLines)
                                
        # Display plot
        plt.show()
            
    def get_border(self, cell, patch):
        # Get vertices to draw our border based on walls present in cell
        verts = patch.get_verts()
        
        # Define border collection
        borders = []
        
        if cell.bottom == 1:
            borders.append(self.bottom_border(verts))
        
        if cell.top == 1:
            borders.append(self.top_border(verts))
            
        if cell.left == 1:
            borders.append(self.left_border(verts))
            
        if cell.right == 1:
            borders.append(self.right_border(verts))
            
        return borders
    
    def bottom_border(self, verts):
        # Return two tuples for the x,y of point 1 and x,y of point 2
        # This will store a line representing the bottom of our rect
        return [(verts[0][0], verts[0][1]), (verts[1][0], verts[1][1])]
    
    def top_border(self, verts):
        return [(verts[3][0], verts[3][1]), (verts[2][0], verts[2][1])]
    
    def left_border(self, verts):
        return [(verts[0][0], verts[0][1]), (verts[3][0], verts[3][1])]
    
    def right_border(self, verts):
        return [(verts[1][0], verts[1][1]), (verts[2][0], verts[2][1])]
        
    def get_cell(self, cell, x, y):
        color = "red"
        if x == 0 and y == self.height - 1:
            color = "green"
        elif x == self.width - 1 and y == 0:
            color = "red"
        elif cell.visited:
            color = "white"
            
        # Get our cell and set, position, size and color (no border)    
        return patches.Rectangle((x, y), self.cellSize, self.cellSize, linewidth=0, facecolor=color, edgecolor="black")
    
    # Draw entry and exit arrows
    # ax.arrow(0, 1, .4, 0, fc='green', ec='green', head_width=0.3, head_length=0.3)
    # ax.arrow(maze.shape[1] - 1, maze.shape[0]  - 2, 0.4, 0, fc='blue', ec='blue', head_width=0.3, head_length=0.3)