import tkinter as tk

class TkCell:
    """Object to store all drawn property ID's of a single cell
    """
    
    def __init__(self, cell: int, top: int, bottom: int, left: int, right: int, text: int) -> None:
        """Object to store all drawn property ID's of a single cell

        Args:
            cell (int): ID for cell face
            top (int): ID for top border
            bottom (int): ID for bottom border
            left (int): ID for left border
            right (int): ID for right border
            text (int): ID for center text
        """
        
        self.cell = cell
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.text = text
        
    def set_color(self, canvas: tk.Canvas, color: str):
        """Set the face color of this cell

        Args:
            canvas (tk.Canvas): Canvas the cell resides in
            color (str): Color to use
        """
        canvas.itemconfig(self.cell, fill=color)
        
    def remove_border(self, canvas: tk.Canvas, border: str):
        """Delete a single border from the cell residing within canvas

        Args:
            canvas (tk.Canvas): Canvas the cell resides in
            border (str): Border to delete (top/bottom/left/right)
        """
        if border == "top":
            canvas.delete(self.top)
        elif border == "bottom":
            canvas.delete(self.bottom)
        elif border == "left":
            canvas.delete(self.left)
        elif border == "right":
            canvas.delete(self.right)
            
    def add_text(self, canvas: tk.Canvas, text: str):
        """Add text to the cell

        Args:
            canvas (tk.Canvas): Canvas the cell resides in
            text (str): Text to add/replace
        """
        canvas.itemconfig(self.text, text=text)
            
        
        
    