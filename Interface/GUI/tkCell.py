import tkinter as tk
from Utility.enums import Border
from Utility.enums import Color

class TkCell:
    """Class to manage all displayed properties of a single cell
    """
    
    def __init__(self, cell: int, top: int, bottom: int, left: int, right: int, text: int) -> None:
        """
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
        
    def set_color(self, canvas: tk.Canvas, color: Color):
        """Set the face color of this cell

        Args:
            canvas (tk.Canvas): Canvas the cell resides in
            color (Enum): Color to use
        """
        canvas.itemconfig(self.cell, fill=color.value)
        
    def remove_border(self, canvas: tk.Canvas, border: Border):
        """Delete a single border from the cell residing within canvas

        Args:
            canvas (tk.Canvas): Canvas the cell resides in
            border (Enum): Border to delete (TOP/BOTTOM/LEFT/RIGHT)
        """
        if border == Border.TOP:
            canvas.delete(self.top)
        elif border == Border.BOTTOM:
            canvas.delete(self.bottom)
        elif border == Border.LEFT:
            canvas.delete(self.left)
        elif border == Border.RIGHT:
            canvas.delete(self.right)
            
    def add_text(self, canvas: tk.Canvas, text: str):
        """Add text to the cell

        Args:
            canvas (tk.Canvas): Canvas the cell resides in
            text (str): Text to add/replace
        """
        canvas.itemconfig(self.text, text=text)
            
        
        
    