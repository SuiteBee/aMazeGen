import tkinter as tk
from Draw.tkGrid import TkGrid

class TkDraw:
    def __init__(self, width: int, height: int, isAnimated: bool) -> None:
        # Canvas that will store the maze
        self.window = tk.Tk()
        self.window.title("Maze Generator")
        
        # Separate canvas for animation controls
        self.controls = None
        
        # Should we update the window after every operation
        self.isAnimated = isAnimated
        # Rate at which updates occur
        self.timeStep = 1
        # Pause switch tied to button press during animation
        self.pauseBtn = None
        self.continueBtn = None
        self.btnCoords = None
        
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
            
    def __set_timestep(self, value: int) -> None:
        self.timeStep = value
            
    def begin_generation(self) -> None:
        """Show a dialog box to pause GUI and set animation timestep if applicable
        """

        if self.isAnimated:
            # Make an update to bring up our maze canvas
            self.window.update()
            
            # Create a popup
            dWidth = 200
            dHeight = 180
            
            self.controls = tk.Toplevel(self.window)
            self.controls.title("Controller")
            self.controls.geometry(f"{dWidth}x{dHeight}")
            self.controls.grab_set()
            
            lbl = tk.Label(self.controls, text="Ready to start?", font=("Arial",12))
            lbl.pack(ipady=10)
            
            # Add a slider to select our timestep
            slider = tk.Scale(self.controls, label="Time Step (ms)", font=("Arial",8), from_=1, to=500, orient=tk.HORIZONTAL, command=self.__set_timestep, variable=self.timeStep)
            slider.pack()

            # Add a button that will destroy itself when pressed
            startButton = tk.Button(self.controls, text="Begin", width=10)
            bPosX = (dWidth/2) - (startButton.winfo_reqwidth()/2)
            bPosY = (dHeight - 60)
            startButton.place(x=bPosX, y=bPosY)
            startButton.config(command=startButton.destroy)
            
            # wait until button is destroyed
            self.controls.wait_window(startButton)
            
            # Create a pause button
            self.pauseBtn = tk.Button(self.controls, text="Pause", width=10, command=self.__pause_anim)
            self.btnCoords=(bPosX,bPosY)
            self.pauseBtn.place(x=bPosX, y=bPosY)
        
    def __pause_anim(self) -> None:
        """Create a continue button and place it above the pause button, wait until it is destroyed
        """
        self.continueBtn = tk.Button(self.controls, text="Continue", width=10)
        self.continueBtn.place(x=self.btnCoords[0], y=self.btnCoords[1])
        self.continueBtn.config(command=self.continueBtn.destroy)
        
        self.pauseBtn.lower(self.continueBtn)
    
        self.controls.wait_window(self.continueBtn)

    def finish_generation(self) -> None:
        """Show a dialog box to pause GUI
        """
        # Open up our entrance/exit and draw arrows
        self.grid.open()
        
        # One more call to update to draw maze if it was not animated
        self.window.update()
        
        # Create a popup
        if self.controls is None:
            self.controls = tk.Toplevel(self.window)
            self.controls.title("Controller")
        else:
            for child in self.controls.winfo_children():
                child.destroy()
        
        # Add some text
        line_one = tk.Label(self.controls, text="Finished Generating Maze", font=("Arial",12))
        line_two = tk.Label(self.controls, text="Ready to Solve?", font=("Arial",10))
            
        if self.isAnimated:
            # Position elements WITH timestep slider
            dWidth = 250
            dHeight = 200
            self.controls.geometry(f"{dWidth}x{dHeight}")
            
            line_one.pack(pady=(10, 0))
            line_two.pack(ipady=0)
        
            # Add a slider to select our timestep
            slider = tk.Scale(self.controls, label="Time Step (ms)", font=("Arial",8), from_=1, to=500, orient=tk.HORIZONTAL, command=self.__set_timestep, variable=self.timeStep)
            slider.pack()

            # Add a button that will destroy itself when pressed
            startButton = tk.Button(self.controls, text="Begin", width=10)
            bPosX = (dWidth/2) - (startButton.winfo_reqwidth()/2)
            bPosY = (dHeight - 50)
            startButton.place(x=bPosX, y=bPosY)
            startButton.config(command=startButton.destroy)
            
            # wait until button is destroyed
            self.controls.wait_window(startButton)
            
            # Create a pause button
            self.pauseBtn = tk.Button(self.controls, text="Pause", width=10, command=self.__pause_anim)
            self.btnCoords=(bPosX,bPosY)
            self.pauseBtn.place(x=bPosX, y=bPosY)
        else:
            # Add a button that will continue execution when closed
            button = tk.Button(self.controls, text="Begin", command=self.controls.destroy, width=10)
        
            # Position elements WITHOUT timestep slider
            dWidth = 250
            dHeight = 120
            self.controls.geometry(f"{dWidth}x{dHeight}")
            
            line_one.pack(pady=(10, 0))
            line_two.pack(ipady=0)
            
            bPosX = (dWidth/2) - (button.winfo_reqwidth()/2)
            bPosY = (dHeight - 50)
            button.place(x=bPosX, y=bPosY)
            
            # Pause until dialog is destroyed
            self.window.wait_window(self.controls)
        
    def finish_solution(self) -> None:
        # Create a popup
        if self.controls is None:
            self.controls = tk.Toplevel(self.window)
            self.controls.title("Controller")
        else:
            for child in self.controls.winfo_children():
                child.destroy()
                
        dWidth = 200
        dHeight = 100
        self.controls.geometry(f"{dWidth}x{dHeight}")
        
        lbl = tk.Label(self.controls, text="Solved", font=("Arial",12))
        lbl.pack(ipady=10)
    
        # Add a button that will continue execution when closed
        button = tk.Button(self.controls, text="Close", command=self.controls.destroy, width=10)
        bPosX = (dWidth/2) - (button.winfo_reqwidth()/2)
        bPosY = (dHeight - 60)
        button.place(x=bPosX, y=bPosY)
        
        # Pause until dialog is destroyed
        self.window.wait_window(self.controls)