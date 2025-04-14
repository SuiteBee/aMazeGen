import matplotlib.patches as patches
import matplotlib.collections as collect

class PlotCell:
    def __init__(self, x: int, y: int, facecolor: str, cellSize: float, borderSize: float) -> None:
        # Retrieve cell shape, size and color
        self.patch = self.__get_rect(x, y, facecolor, cellSize)

        # Get collection of border lines for cell
        self.borderSize = borderSize
        self.borders = self.__get_borders()
        
    def set_patch_color(self, facecolor: str) -> None:
        """Set color of cell
        """
        
        self.patch.set_facecolor(facecolor)
        
    def set_border_active(self, index: int, active: bool) -> None:
        """Set border to be visible by replacing the line collection widths array
        Line collection does not allow for altering list elements directly
        """
        
        # Get list of our border widths for all four borders
        current = self.borders.get_linewidth()

        # Alter the specified border width
        current[index] = self.borderSize if active else 0
        
        # Replace the border widths collection with our altered version
        self.borders.set_linewidth(current)

    def __get_rect(self, x: int, y: int, facecolor: str, cellSize: float) -> patches.Rectangle:
        """Return square representing our cell with origin at x,y
        """
        
        # Get our rect and set, position, size and color (no border we need to draw these individually)    
        return patches.Rectangle((x, y), cellSize, cellSize, linewidth=0, facecolor=facecolor, edgecolor="black")  
    
    def __get_borders(self) -> collect.LineCollection:
        """Get borders of this plot cell by referencing vertices and storing four lines in a collection
        Patch does not allow for accessing borders individually
        """
        
        # Get vertices to draw our border based on walls present in cell
        verts = self.patch.get_verts()
        
        # Define border line collection
        borders = []
        
        borders.append(self.__bottom_border(verts))
        borders.append(self.__top_border(verts))
        borders.append(self.__left_border(verts))
        borders.append(self.__right_border(verts))
        
        # Define border widths initially active
        linewidths = [self.borderSize] * 4
            
        return collect.LineCollection(borders, edgecolors="black", linewidths=linewidths)
    
    def __bottom_border(self, verts: list[list[int]]) -> list[tuple]:
        """
        Args:
            verts (list[list[int]]): All vertices for a given patch

        Returns:
            list[tuple]: Tuples representing two lower vertices we will connect with a line
        """
        
        # Return two tuples for the x,y of point 1 and x,y of point 2
        # This will store a line representing the bottom of our rect
        return [(verts[0][0], verts[0][1]), (verts[1][0], verts[1][1])]

    def __top_border(self, verts: list[list[int]]) -> list[tuple]:
        """
        Args:
            verts (list[list[int]]): All vertices for a given patch

        Returns:
            list[tuple]: Tuples representing two upper vertices we will connect with a line
        """
        
        return [(verts[3][0], verts[3][1]), (verts[2][0], verts[2][1])]

    def __left_border(self, verts: list[list[int]]) -> list[tuple]:
        """
        Args:
            verts (list[list[int]]): All vertices for a given patch

        Returns:
            list[tuple]: Tuples representing two left vertices we will connect with a line
        """
        
        return [(verts[0][0], verts[0][1]), (verts[3][0], verts[3][1])]

    def __right_border(self, verts: list[list[int]]) -> list[tuple]:
        """
        Args:
            verts (list[list[int]]): All vertices for a given patch

        Returns:
            list[tuple]: Tuples representing two right vertices we will connect with a line
        """
        
        return [(verts[1][0], verts[1][1]), (verts[2][0], verts[2][1])]
        
    