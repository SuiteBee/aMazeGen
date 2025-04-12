import matplotlib.patches as patches
import matplotlib.collections as collect

class PlotCell:
    def __init__(self, cell, x, y, facecolor, cellSize, borderSize):
        # Retrieve cell shape, size and color
        self.patch = self.__get_rect(x, y, facecolor, cellSize)
        # Get collection of border lines for cell
        self.borders = self.__get_borders(cell, borderSize)
        # Erase borders
        self.eraseBorders = self.__erase_borders(borderSize)

    def __get_rect(self, x, y, facecolor, cellSize=1):
        # Get our rect and set, position, size and color (no border we need to draw these individually)    
        return patches.Rectangle((x, y), cellSize, cellSize, linewidth=0, facecolor=facecolor, edgecolor="black")  
    
    def __erase_borders(self, borderSize=1):
        # Get vertices to draw our border based on walls present in cell
        verts = self.patch.get_verts()
        
        # Define border collection
        borders = []
        # Bottom
        borders.append(self.__bottom_border(verts))
        # Top
        borders.append(self.__top_border(verts))
        # Left
        borders.append(self.__left_border(verts))
        # Right
        borders.append(self.__right_border(verts))
            
        return collect.LineCollection(borders, edgecolors="white", linewidths=borderSize)
    
    def __get_borders(self, cell, borderSize=1):
        # Get vertices to draw our border based on walls present in cell
        verts = self.patch.get_verts()
        
        # Define border collection
        borders = []
        
        if cell.bottom == 1:
            borders.append(self.__bottom_border(verts))
        
        if cell.top == 1:
            borders.append(self.__top_border(verts))
            
        if cell.left == 1:
            borders.append(self.__left_border(verts))
            
        if cell.right == 1:
            borders.append(self.__right_border(verts))
            
        return collect.LineCollection(borders, edgecolors="black", linewidths=borderSize)
    
    def __bottom_border(self, verts):
        # Return two tuples for the x,y of point 1 and x,y of point 2
        # This will store a line representing the bottom of our rect
        return [(verts[0][0], verts[0][1]), (verts[1][0], verts[1][1])]
    
    def __top_border(self, verts):
        return [(verts[3][0], verts[3][1]), (verts[2][0], verts[2][1])]
    
    def __left_border(self, verts):
        return [(verts[0][0], verts[0][1]), (verts[3][0], verts[3][1])]
    
    def __right_border(self, verts):
        return [(verts[1][0], verts[1][1]), (verts[2][0], verts[2][1])]
        
    