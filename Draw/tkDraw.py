import tkinter as tk
from Draw.tkGrid import TkGrid

class TkDraw:
    def __init__(self, root: tk.Tk, isAnimated: bool, width: int, height: int) -> None:
        # Canvas that stores the maze
        self.window = root
        
        # Should we update the window after every operation
        self.isAnimated = isAnimated
        # Rate at which updates occur
        self.timeStep = 1
        
        # A container for frames to render
        self.frame_queue: list[tuple[tuple[int,int],tuple[str,str]]] = []
        
        # Graphic representation of our maze
        self.grid = TkGrid(root, width, height)
        
    def queue_frame(self, address: tuple[int,int], instruction: tuple[str,str]) -> None:
        """Append a cell alteration to a queue to be completed and emptied by calling draw_pending()
        
        Allows for multiple changes without waiting for update(timeStep)
        """
        
        self.frame_queue.append((address, instruction))

    def draw_pending(self) -> None:
        """Step through elements in the frame queue and if animated update after completion of all frames
        """
        
        while len(self.frame_queue) > 0:
            step = self.frame_queue.pop()
            address = step[0]
            instruction = step[1]
            self.grid.modify(address, instruction)
            
        if self.isAnimated:
            self.window.after(self.timeStep, self.window.update())
        
    def draw_frame(self, address: tuple[int,int], instruction: tuple[str,str]) -> None:   
        """Modify grid cell at address (x,y) and update if animated
        """
        
        self.grid.modify(address, instruction)
        
        if self.isAnimated:
            self.window.after(self.timeStep, self.window.update())