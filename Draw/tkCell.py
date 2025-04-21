import tkinter as tk

class TkCell:
    def __init__(self, cell, top, bottom, left, right, text) -> None:
        """TkCells will store objectId's for the cell iteslf as well as its four borders
        """
        self.cell = cell
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.text = text
        
    def set_color(self, canvas: tk.Canvas, color):
        canvas.itemconfig(self.cell, fill=color)
        
    def remove_border(self, canvas: tk.Canvas, border):
        if border == "top":
            canvas.itemconfig(self.top, fill="white")
        elif border == "bottom":
            canvas.itemconfig(self.bottom, fill="white")
        elif border == "left":
            canvas.itemconfig(self.left, fill="white")
        elif border == "right":
            canvas.itemconfig(self.right, fill="white")
            
    def add_text(self, canvas: tk.Canvas, text):
        canvas.itemconfig(self.text, text=text)
            
        
        
    