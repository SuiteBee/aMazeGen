import tkinter as tk
from Interface.GUI.tkDraw import TkDraw
from Interface.GUI.tkElements import TkElements

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
        self.controls: tk.Frame = None
        # Frame to display maze information
        self.info: tk.Frame = None

        # Pause switch tied to button press during animation
        self.pause_btn: tk.Button = None
        self.continue_btn: tk.Button = None
        self.btn_coords = None
        
        # Repeat switch tied to button press after solving
        self.repeat = False

    def begin_generation(self, gen) -> None:
        """Show a dialog box to pause GUI and set animation timestep if applicable
        """

        if self.isAnimated:
            # Make an update to bring up our maze canvas
            self.window.update()

            # Get our control panel
            self.__get_controls()
            
            TkElements.set_generation_text(self.controls, 0.3)
            TkElements.set_slider(self.controls, 0.38, self.__set_timestep, self.animator.timeStep)
            
            # Create a button that will destroy itself when pressed
            start_button: tk.Button = TkElements.get_start_button(self.controls, 0.6)
            self.controls.update()
            # Take note of button position to create a pause/continue
            self.btn_coords=(start_button.winfo_x(),start_button.winfo_y())

            # Display info about generation bottom right
            TkElements.set_generation_info(self.info, 0.2, gen)
            
            # Wait until start button is destroyed
            self.controls.wait_window(start_button)
            
            self.pause_btn = TkElements.get_pause_button(self.controls, self.btn_coords, self.__pause_anim)

    def finish_generation(self, solve) -> None:
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
            
            TkElements.set_solution_text(self.controls, 0.3)
            TkElements.set_slider(self.controls, 0.5, self.__set_timestep, self.animator.timeStep)
            
            # Create a button that will destroy itself when pressed
            start_button: tk.Button = TkElements.get_start_button(self.controls, 0.73)
            # Take note of button position to create a pause/continue
            self.controls.update()
            self.btn_coords=(start_button.winfo_x(),start_button.winfo_y())
            
            # Display info about solution bottom right
            TkElements.set_solution_info(self.info, 0.2, solve)
    
            # Wait until start button is destroyed
            self.controls.wait_window(start_button)
            
            self.pause_btn = TkElements.get_pause_button(self.controls, self.btn_coords, self.__pause_anim)
        else:
            # Position elements WITHOUT timestep slider
            # Get our control panel
            self.__get_controls()

            TkElements.set_solution_text(self.controls, 0.3)
            
            # Create a button that will destroy itself when pressed
            start_button = TkElements.get_start_button(self.controls, 0.55)
            
            # Display info about solution bottom right
            TkElements.set_solution_info(self.info, 0.2, solve)
            
            # Wait until start button is destroyed
            self.controls.wait_window(start_button)
        
    def finish_solution(self) -> bool:
        """Show a dialog box to pause GUI and see solution before close
        
        Give option to run the algorithm again and return a variable depending on which button is pressed
        """
        # Get our control panel
        self.__get_controls()
        
        TkElements.set_finish_text(self.controls, 0.3)

        # Add a button that will set a repeat variable and destroy the window
        TkElements.get_repeat_button(self.controls, 0.45, self.__repeat)
        
        # Add a button that will destroy the window when pressed
        TkElements.get_close_button(self.controls, 0.65, self.__close)
        
        # Create a trigger to pause execution until user interaction (for some reason this has to be set to an unused variable to function)
        button_press = tk.BooleanVar(self.controls, name="trigger", value=False)
        
        # Wait until trigger is fired
        self.controls.wait_variable("trigger")
        
        return self.repeat
        
    def __get_controls(self) -> None:
        """Create control panel if none exists or wipe out controls + info to reset
        """
        if self.controls is None:
            # Outer frame to fill right side
            outer = TkElements.get_main_panel(self.window)
            
            # Top Section
            TkElements.set_title(outer)
            
             # Middle Section
            self.controls = TkElements.get_control_panel(outer)
            
            # Bottom section
            self.info = TkElements.get_info_panel(outer)

        elif len(self.controls.winfo_children()) > 0:
            for child in self.controls.winfo_children():
                child.destroy()
                
            if len(self.info.winfo_children()) > 0:
                for child in self.info.winfo_children():
                    child.destroy()

    def __set_timestep(event, value: int) -> None:
        """Set the animation timestep in milliseconds
        """
        event.animator.timeStep = value
            
    def __pause_anim(event) -> None:
        """Create a continue button and place it above the pause button, wait until it is destroyed
        """
        event.continue_btn = TkElements.get_continue_button(event.controls, event.btn_coords)
        
        # Place pause button below continue
        event.pause_btn.lower(event.continue_btn)
    
        # Wait until continue is pressed
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