import tkinter as tk
from Interface.GUI.tkDraw import TkDraw

class TkController:
    """Root class to control application events and update the control panel
    """
    
    def __init__(self, width: int, height: int, isAnimated: bool) -> None:
        # Main root application window
        self.window = tk.Tk()
        self.window.title("Maze Generator")
        self.window.protocol("WM_DELETE_WINDOW", self.__exit)
        self.window.resizable(False, False)
        
        # Should we update the window after every operation
        self.isAnimated = isAnimated
        self.animator = TkDraw(self.window, isAnimated, width, height)
        
        # Frame to house controls
        self.controls = None

        # Pause switch tied to button press during animation
        self.pause_btn = None
        self.continue_btn = None
        self.btn_coords = None
        
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
            slider.set(self.animator.timeStep)
            slider.place(relx=0.5, rely=0.45, anchor="center")

            # Add a button that will destroy itself when pressed
            start_button = tk.Button(self.controls, text="Begin", font=("Arial",16), width=18, height=2)
            start_button.config(command=start_button.destroy)         
            start_button.place(relx=0.5, rely=0.6, anchor="center")
            self.controls.update()
            self.btn_coords=(start_button.winfo_x(),start_button.winfo_y())
            
            # Wait until start button is destroyed
            self.controls.wait_window(start_button)
            
            # Create a pause button
            self.pause_btn = tk.Button(
                self.controls, text="Pause", font=("Arial",16), 
                width=18, height=2, command=self.__pause_anim
            )
            self.pause_btn.place(x=self.btn_coords[0], y=self.btn_coords[1])

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
            slider.set(self.animator.timeStep)
            slider.place(relx=0.5, rely=0.58, anchor="center")

            # Add a button that will destroy itself when pressed
            start_button = tk.Button(self.controls, text="Begin", font=("Arial",16), width=18, height=2)
            start_button.config(command=start_button.destroy)
            start_button.place(relx=0.5, rely=0.73, anchor="center")
            self.controls.update()
            self.btn_coords=(start_button.winfo_x(),start_button.winfo_y())
    
            # Wait until start button is destroyed
            self.controls.wait_window(start_button)
            
            # Create a pause button
            self.pause_btn = tk.Button(
                self.controls, text="Pause", font=("Arial",16), 
                width=18, height=2, command=self.__pause_anim
            )
            self.pause_btn.place(x=self.btn_coords[0], y=self.btn_coords[1])
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
            start_button = tk.Button(self.controls, text="Begin", font=("Arial",16), width=18, height=2)
            start_button.config(command=start_button.destroy)      
            start_button.place(relx=0.5, rely=0.55, anchor="center")

            # Wait until start button is destroyed
            self.controls.wait_window(start_button)
        
    def finish_solution(self) -> bool:
        """Show a dialog box to pause GUI and see solution before close
        
        Give option to run the algorithm again and return a variable depending on which button is pressed
        """
        # Get our control panel
        self.__get_controls()
        
        lbl = tk.Label(self.controls, text="Finished Solving", font=("Arial",24))
        lbl.place(relx=0.5, rely=0.3, anchor="center")

        # Add a button that will set a repeat variable and destroy the window
        repeat_button = tk.Button(self.controls, text="Solve Again", font=("Arial",16), width=18, height=2)
        repeat_button.config(command=self.__repeat)
        repeat_button.place(relx=0.5, rely=0.45, anchor="center")
        
        # Add a button that will destroy the window when pressed
        close_button = tk.Button(self.controls, text="Close", font=("Arial",16), width=18, height=2)
        close_button.config(command=self.__close)
        close_button.place(relx=0.5, rely=0.65, anchor="center")
        
        # Create a trigger to pause execution until user interaction
        button_press = tk.BooleanVar(self.controls, name="trigger", value=False)
        
        # Wait until trigger is fired
        self.controls.wait_variable("trigger")
        
        return self.repeat
        
    def __get_controls(self) -> None:
        """Assign a new frame to house the controls
        """
        if self.controls is None:
            # Outer frame to fill right side
            outer = tk.Frame(self.window, width=350,
                highlightbackground="black", highlightthickness=3
            )
            outer.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
            
            # Inner frame that will not resize to keep widgets organized
            self.controls = tk.Frame(outer, width=350, height=500)
            # Stop frame from resizing
            self.controls.pack_propagate(0)
            self.controls.pack(side=tk.RIGHT, expand=True)

        elif len(self.controls.winfo_children()) > 0:
            for child in self.controls.winfo_children():
                child.destroy()

    def __set_timestep(event, value: int) -> None:
        """Set the animation timestep in milliseconds
        """
        event.animator.timeStep = value
            
    def __pause_anim(event) -> None:
        """Create a continue button and place it above the pause button, wait until it is destroyed
        """
        event.continue_btn = tk.Button(event.controls, text="Continue", font=("Arial",16), width=18, height=2)
        event.continue_btn.place(x=event.btn_coords[0], y=event.btn_coords[1])
        event.continue_btn.config(command=event.continue_btn.destroy)
        
        event.pause_btn.lower(event.continue_btn)
    
        event.controls.wait_window(event.continue_btn)
        
    def __repeat(event) -> None:
        """Set a loop variable
        """
        event.__trigger()
        event.repeat = True
        
    def __close(event) -> bool:
        """Stop loop and close window
        """
        event.__trigger()
        event.repeat = False
        
        event.window.quit()
        event.window.destroy()
        
    def __exit(event):
        event.__trigger()
        event.window.quit()
        event.window.destroy()
        
    def __trigger(event) -> None:
        # Try to set trigger if application is waiting, this will sometimes not exist
        try:
            val = event.controls.getvar("trigger")
            event.controls.setvar("trigger", not val)
        except:
            pass