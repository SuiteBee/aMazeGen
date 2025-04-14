import matplotlib.patches as patches
import matplotlib.collections as collect

class PlotCell:
    def __init__(self, x, y, facecolor, cellSize, borderSize):
        # Retrieve cell shape, size and color
        self.patch = self.__get_rect(x, y, facecolor, cellSize)

        # Get collection of border lines for cell
        self.borderSize = borderSize
        self.borders = self.__get_borders()
        
    def set_patch_color(self, facecolor):
        self.patch.set_facecolor(facecolor)
        
    def set_border_active(self, index, active):
        current = self.borders.get_linewidth()

        current[index] = self.borderSize if active else 0
        self.borders.set_linewidth(current)

    def __get_rect(self, x, y, facecolor, cellSize=1):
        # Get our rect and set, position, size and color (no border we need to draw these individually)    
        return patches.Rectangle((x, y), cellSize, cellSize, linewidth=0, facecolor=facecolor, edgecolor="black")  
    
    def __get_borders(self):
        # Get vertices to draw our border based on walls present in cell
        verts = self.patch.get_verts()
        
        # Define border line collection
        borders = []
        
        borders.append(self.__bottom_border(verts))
        borders.append(self.__top_border(verts))
        borders.append(self.__left_border(verts))
        borders.append(self.__right_border(verts))
        
        # Define border widths initially 0
        linewidths = [self.borderSize] * 4
            
        return collect.LineCollection(borders, edgecolors="black", linewidths=linewidths)
    
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
        
    