import tkinter as tk

from Draw.tkDraw import TkDraw

class TkController:
    def __init__(self, width: int, height: int, isAnimated: bool) -> None:
        # Canvas that will store the maze
        self.window = tk.Tk()
        self.window.title("Maze Generator")
        
        # Should we update the window after every operation
        self.isAnimated = isAnimated
        self.animator = TkDraw(self.window, isAnimated, width, height)
        
        # Frame to house controls
        self.controls = None

        # Pause switch tied to button press during animation
        self.pauseBtn = None
        self.continueBtn = None
        self.btnCoords = None
        
        # Repeat switch tied to button press after solving
        self.repeat = False

    def begin_generation(self) -> None:
        """Show a dialog box to pause GUI and set animation timestep if applicable
        """

        if self.isAnimated:
            # Make an update to bring up our maze canvas
            self.window.update()

            # Get our control panel
            self.__get_controls()
            
            lbl = tk.Label(self.controls, text="Ready to start?", font=("Arial",24))
            lbl.place(relx=0.5, rely=0.3, anchor="center")
            
            sld_lbl = tk.Label(self.controls, text="Time Step (ms)", font=("Arial",16))
            sld_lbl.place(relx=0.5, rely=0.38, anchor="center")
            
            # Add a slider to select our timestep
            slider = tk.Scale(
                self.controls, from_=1, to=500, length=250,
                orient=tk.HORIZONTAL, 
                command=self.__set_timestep, 
                variable=self.animator.timeStep
            )
            
            slider.place(relx=0.5, rely=0.45, anchor="center")

            # Add a button that will destroy itself when pressed
            startButton = tk.Button(self.controls, text="Begin", font=("Arial",16), width=18, height=2)
            startButton.config(command=startButton.destroy)         
            startButton.place(relx=0.5, rely=0.6, anchor="center")
            self.controls.update()
            self.btnCoords=(startButton.winfo_x(),startButton.winfo_y())
            
            # wait until button is destroyed
            self.controls.wait_window(startButton)
            
            # Create a pause button
            self.pauseBtn = tk.Button(
                self.controls, text="Pause", font=("Arial",16), 
                width=18, height=2, command=self.__pause_anim
            )
            self.pauseBtn.place(x=self.btnCoords[0], y=self.btnCoords[1])

    def finish_generation(self) -> None:
        """Show a dialog box to pause GUI and set animation timestep if applicable
        """
        # Open up our entrance/exit and draw arrows
        self.animator.grid.open()
        
        # One more call to update to draw maze if it was not animated
        self.window.update()
            
        if self.isAnimated:
            # Position elements WITH timestep slider
            # Get our control panel
            self.__get_controls()
            
            # Add some text
            line_one = tk.Label(self.controls, text="Finished Generating", font=("Arial",24))
            line_one.place(relx=0.5, rely=0.3, anchor="center")
            line_two = tk.Label(self.controls, text="Ready to Solve?", font=("Arial",16))
            line_two.place(relx=0.5, rely=0.38, anchor="center")
        
            # Add a slider to select our timestep
            sld_lbl = tk.Label(self.controls, text="Time Step (ms)", font=("Arial",16))
            sld_lbl.place(relx=0.5, rely=0.5, anchor="center")
            
            # Add a slider to select our timestep
            slider = tk.Scale(
                self.controls, from_=1, to=500, length=250,
                orient=tk.HORIZONTAL, 
                command=self.__set_timestep, 
                variable=self.animator.timeStep
            )
            
            slider.place(relx=0.5, rely=0.58, anchor="center")

            # Add a button that will destroy itself when pressed
            startButton = tk.Button(self.controls, text="Begin", font=("Arial",16), width=18, height=2)
            startButton.config(command=startButton.destroy)
            startButton.place(relx=0.5, rely=0.73, anchor="center")
            self.controls.update()
            self.btnCoords=(startButton.winfo_x(),startButton.winfo_y())
            
            # wait until button is destroyed
            self.controls.wait_window(startButton)
            
            # Create a pause button
            self.pauseBtn = tk.Button(
                self.controls, text="Pause", font=("Arial",16), 
                width=18, height=2, command=self.__pause_anim
            )
            self.pauseBtn.place(x=self.btnCoords[0],y=self.btnCoords[1])
        else:
            # Position elements WITHOUT timestep slider
            # Get our control panel
            self.__get_controls()
            
            # Add some text
            line_one = tk.Label(self.controls, text="Finished Generating", font=("Arial",24))
            line_one.place(relx=0.5, rely=0.3, anchor="center")
            line_two = tk.Label(self.controls, text="Ready to Solve?", font=("Arial",16))
            line_two.place(relx=0.5, rely=0.38, anchor="center")
            
            # Add a button that will destroy itself when pressed
            startButton = tk.Button(self.controls, text="Begin", font=("Arial",16), width=18, height=2)
            startButton.config(command=startButton.destroy)      
            startButton.place(relx=0.5, rely=0.55, anchor="center")
            
            # wait until button is destroyed
            self.controls.wait_window(startButton)
        
    def finish_solution(self) -> bool:
        """Show a dialog box to pause GUI and see solution before close
        
        Give option to run the algorithm again and return a variable depending on which button is pressed
        """
        # Get our control panel
        self.__get_controls()
        
        lbl = tk.Label(self.controls, text="Finished Solving", font=("Arial",24))
        lbl.place(relx=0.5, rely=0.3, anchor="center")

        # Add a button that will set a repeat variable and destroy the window
        repeatButton = tk.Button(self.controls, text="Solve Again", font=("Arial",16), width=18, height=2)
        repeatButton.config(command=self.__repeat)
        repeatButton.place(relx=0.5, rely=0.4, anchor="center")
        
        # Add a button that will destroy the window when pressed
        closeButton = tk.Button(self.controls, text="Close", font=("Arial",16), width=18, height=2)
        closeButton.config(command=self.__close)
        closeButton.place(relx=0.5, rely=0.5, anchor="center")
        
        # wait until window is destroyed
        self.controls.wait_window(self.controls)
        
        return self.repeat
        
    def __get_controls(self) -> None:
        """Assign a new frame to house the controls
        """
        if self.controls is None:
            self.controls = tk.Frame(
                self.window, width=350, height=500, 
                highlightbackground="black", highlightthickness=3
            )
            
            # Stop frame from resizing
            self.controls.pack_propagate(0)
            self.controls.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

        elif len(self.controls.winfo_children()) > 0:
            for child in self.controls.winfo_children():
                child.destroy()

    def __set_timestep(self, value: int) -> None:
        self.animator.timeStep = value
            
    def __pause_anim(self) -> None:
        """Create a continue button and place it above the pause button, wait until it is destroyed
        """
        self.continueBtn = tk.Button(self.controls, text="Continue", font=("Arial",16), width=18, height=2)
        self.continueBtn.place(x=self.btnCoords[0], y=self.btnCoords[1])
        self.continueBtn.config(command=self.continueBtn.destroy)
        
        self.pauseBtn.lower(self.continueBtn)
    
        self.controls.wait_window(self.continueBtn)
        
    def __repeat(self) -> None:
        """Set a loop variable to control output and reset the control panel
        """
     
        self.repeat = True
        self.controls.destroy()
        self.controls = None
        
    def __close(self) -> bool:
        """Stop loop and reset control panel
        """
        
        self.repeat = False
        self.controls.destroy()
        self.controls = None