import tkinter as tk

from Draw.tkCell import TkCell

class TkGrid:
    def __init__(self, root: tk.Tk, width: int, height: int):
        self.width = width
        self.height = height

        # Physical screen dimensions in pixels
        self.screen_size = self.__get_screen_size(root)
        # Target is 70% of screen size before adjusting based on aspect
        self.target_width = round(.7 * self.screen_size[0], 0)
        self.target_height = round(.7 * self.screen_size[1], 0)
        
        # Extra space at edge of frame
        self.frame_padding = 80
        # Outer cell padding
        self.cell_padding = 40
        
        # Cell size is determined by our final canvas size
        self.cell_size = -1
        # Shrink edge width for large grids
        self.edge_width = 1 if width + height > 100 else 3
              
        self.canvas = self.__get_canvas(root)
        self.cells = self.__generate_grid()
        
    def modify(self, address: tuple[int,int], instruction: tuple[str,str]) -> None:
        """Perform instruction operation on cell at address(x,y)
        
        This can color the cell face, hide a specified border or add text
        
        Usage 
            modify((x,y), ("cell", "red"))
            modify((x,y), ("border", "top/bottom/left/right"))
            modify((x,y), ("text", "str"))
        """
        x = address[0]
        y = address[1]
        
        part = instruction[0]

        if part == "cell":
            color = instruction[1]
            self.cells[x][y].set_color(self.canvas, color)
        elif part == "border":
            border = instruction[1]
            self.cells[x][y].remove_border(self.canvas, border)
        elif part == "text":
            text = instruction[1]
            self.cells[x][y].add_text(self.canvas, text)
            
    def open(self) -> None:
        """Open entry/exit cells and draw arrow
        """

        # Set entry and exit (top left, bottom right)
        self.modify((0, self.height - 1), ("border", "left"))
        self.modify((self.width - 1, 0), ("border", "right"))
        
        # Draw entry arrow
        entryX1 = self.cell_padding/4
        entryY1 = self.cell_size/2 + self.cell_padding
        entryX2 = self.cell_padding - self.cell_padding/4
        entryY2 = self.cell_size/2 + self.cell_padding
        
        self.canvas.create_line(entryX1, entryY1, entryX2, entryY2, arrow=tk.LAST, fill="black", width=3)
        
        # Get our bottom right cell text (already at half height)
        bottom_right: TkCell = self.cells[self.width - 1][0]
        exit_pos = self.canvas.coords(bottom_right.text)

        # Draw exit arrow
        exitX1 = exit_pos[0] + self.cell_size/2 + self.cell_padding/4
        exitY1 = exit_pos[1]
        exitX2 = exit_pos[0] + self.cell_size/2 + self.cell_padding - self.cell_padding/4
        exitY2 = exit_pos[1]
        
        self.canvas.create_line(exitX1, exitY1, exitX2, exitY2, arrow=tk.LAST, fill="black", width=3)
        
    def __get_screen_size(self, root: tk.Tk) -> tuple[int,int]:
        """Set to full screen, grab dimensions and set back
        
        Return a tuple with (width, height) in pixels
        """
        
        root.update_idletasks()
        root.attributes("-fullscreen", True)
        dimensions = root.winfo_geometry().split("+")[0]
        root.attributes("-fullscreen", False)
        
        screen_width = int(dimensions.split("x")[0])
        screen_height = int(dimensions.split("x")[1])
        return (screen_width, screen_height)
        
    def __get_canvas(self, root: tk.Tk) -> tk.Canvas:
        """Determine frame size based on target dimensions and aspect 
        """

        aspect = self.width/self.height
        canvas_width = -1
        canvas_height = -1
        
        # Height is same or greater than width
        if self.target_width / self.target_height >= aspect:
            # Adjust width to allow only necessary amount of space
            canvas_width = int(self.target_height * aspect)
            canvas_height = self.target_height

            # Divide our canvas width by number of columns to get cell size
            # This will ensure our cells fit in the window bounds
            self.cell_size = canvas_width / self.width
        # Width is greater than height
        else:
            canvas_width = self.target_width
            canvas_height = int(self.target_width / aspect)

            self.cell_size = canvas_height / self.height
            
        # Include some white space at the edges
        canvas_width += self.frame_padding
        canvas_height += self.frame_padding

        # Instantiate our canvas object with calculated dimensions and white background
        tmp_canvas = tk.Canvas(
            root, width=canvas_width, height=canvas_height, bg="gray",
            highlightbackground="black", highlightthickness=3
        )
        tmp_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        
        return tmp_canvas
    
    def __generate_grid(self) -> list[list[TkCell]]:
        """Create a 2d list representation of our maze with TkCells
        """
        
        tmp = [[0 for y in range(self.height)] for x in range(self.width)]
        
        for x in range(self.width):
            for y in range(self.height):
                # Set our origin point for our cell and set the oppposing corner based on size
                origin = (x * self.cell_size, y * self.cell_size)
                opposite = (origin[0] + self.cell_size, origin[1] + self.cell_size)
                
                # Generate our cell object and add to array
                tkCell = self.__generate_cell(origin, opposite, "black")
                tmp[x][y] = tkCell
                
        return tmp
    
    def __generate_cell(self, point1: tuple[int,int], point2: tuple[int,int], cellColor: str) -> TkCell:
        """Generate a square with origin at point1 and draw borders using the vertice between point1 and opposing corner point2
        """
        
        # Convert our points from logical space to screen space
        x1,y1 = self.__adjust_point(point1)
        x2,y2 = self.__adjust_point(point2)
        
        # Create our cell face
        cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill=cellColor, outline="")
        
        # Using our cell vertices, determine our border lines
        top = self.canvas.create_line(x1, y2, x2, y2, fill="black", width=self.edge_width)
        bottom = self.canvas.create_line(x1, y1, x2, y1, fill="black", width=self.edge_width)
        left = self.canvas.create_line(x1, y1, x1, y2, fill="black", width=self.edge_width)
        right = self.canvas.create_line(x2, y1, x2, y2, fill="black", width=self.edge_width)
        
        # Create a text field in the center of our cell
        half_width = self.cell_size/2
        x1 += half_width
        y1 -= half_width
        text = self.canvas.create_text(x1, y1, fill="black", text="")
        
        return TkCell(cell, top, bottom, left, right, text)

    # Position our points on the canvas so that 0,0 is bottom,left and add padding
    def __adjust_point(self, point: tuple[int,int]) -> tuple[int,int]:
        """Add padding to x,y coordinates and reverse y axis
        """
        x = point[0] + self.cell_padding
        y = self.__reverse_coordinate(point[1] + self.cell_padding)
        
        return (x,y)

    # 0,0 in GUI is top, left we want to reverse the y coordinate so 0,0 is bottom, left
    def __reverse_coordinate(self, yCoord: int) -> int:
        """Subtract the given y coordinate from the canvas height
        """
        return self.canvas.winfo_reqheight() - yCoord

    