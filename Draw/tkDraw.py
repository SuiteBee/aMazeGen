import tkinter as tk
from Draw.tkGrid import TkGrid

class TkDraw:
    def __init__(self, width: int, height: int, isAnimated: bool) -> None:
        self.window = tk.Tk()
        self.window.title("Maze Generator")
        
        # Should we update the window after every operation
        self.isAnimated = isAnimated
        # Rate at which updates occur
        self.timeStep = 1
        
        # A container for frames to render
        self.frame_queue: list[tuple[tuple[int,int],tuple[str,str]]] = []
        
        # Graphic representation of our maze
        self.grid = TkGrid(self.window, width, height)
        
    def queue_frame(self, address: tuple[int,int], instruction: tuple[str,str]) -> None:
        """Append a cell alteration to a queue to be completed and emptied by calling draw_multiple()
        
        Allows for multiple changes without waiting for update(timeStep)
        """
        
        self.frame_queue.append((address, instruction))

    def draw_multiple(self) -> None:
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
            
    def finish_generation(self) -> None:
        """Show a dialog box to pause GUI
        """
        # Open up our entrance/exit and draw arrows
        self.grid.open()
        
        # One more call to update to draw maze if it was not animated
        self.window.update()
        
        # Create a popup
        dWidth = 200
        dHeight = 100
        dialog = tk.Toplevel(self.window)
        dialog.geometry(f"{dWidth}x{dHeight}")
        
        line_one = tk.Label(dialog, text="Finished Generating Maze")
        line_one.pack()
        line_two = tk.Label(dialog, text="Ready to solve?")
        line_two.pack()

        # Add a button that will continue execution when closed
        button = tk.Button(dialog, text="Continue", command=dialog.destroy)
        bPosX = (dWidth/2) - (button.winfo_reqwidth()/2)
        bPosY = (dHeight - 40)
        button.place(x=bPosX, y=bPosY)
        
        # Pause until dialog is destroyed
        self.window.wait_window(dialog)
        
    def begin_solution(self) -> None:
        pass