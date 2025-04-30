import tkinter as tk

class TkElements:
    """Static class to retrieve all the UI elements
    """
    
    Title_1 = ("Fixedsys", 36, "bold")
    Title_2 = ("Gabriola", 36)
    Header = ("Arial", 24, "bold")
    Subtext = ("Arial", 16)
    
    def get_main_panel(root: tk.Tk) -> tk.Frame:
        panel = tk.Frame(root, width=350, highlightbackground="black", highlightthickness=3)
        panel.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        return panel
        
    def get_control_panel(root: tk.Frame) -> tk.Frame:
        controls = tk.Frame(root, width=350, height=500)
        controls.pack(anchor="center", expand=True)
        return controls
    
    def get_info_panel(root: tk.Frame) -> tk.Frame:
        info = tk.Frame(root, width=350, height=200)
        info.pack(side=tk.BOTTOM)
        return info
    
    def get_start_button(root: tk.Frame, pos: float) -> tk.Button:
        start_button = tk.Button(root, text="Begin", font=TkElements.Subtext, width=18, height=2)
        start_button.config(command=start_button.destroy)
        start_button.place(relx=0.5, rely=pos, anchor="center")
        return start_button
    
    def get_pause_button(root: tk.Frame, pos: tuple[int,int], event) -> tk.Button:
        pause_button = tk.Button(root, text="Pause", font=TkElements.Subtext, width=18, height=2, command=event)
        pause_button.place(x=pos[0], y=pos[1])
        return pause_button
    
    def get_continue_button(root: tk.Frame, pos: tuple[int,int]) -> tk.Button:
        continue_btn = tk.Button(root, text="Continue", font=TkElements.Subtext, width=18, height=2)
        continue_btn.place(x=pos[0], y=pos[1])
        continue_btn.config(command=continue_btn.destroy)
        return continue_btn
    
    def get_repeat_button(root: tk.Frame, pos: float, event) -> tk.Button:
        repeat_button = tk.Button(root, text="Solve Again", font=TkElements.Subtext, width=18, height=2)
        repeat_button.config(command=event)
        repeat_button.place(relx=0.5, rely=pos, anchor="center")
        return repeat_button
    
    def get_close_button(root: tk.Frame, pos: float, event) ->  tk.Button:
        close_button = tk.Button(root, text="Close", font=TkElements.Subtext, width=18, height=2)
        close_button.config(command=event)
        close_button.place(relx=0.5, rely=pos, anchor="center")
        return close_button

    def set_title(root: tk.Frame) -> None:
        title = tk.Frame(root, width=350, height=100)
        title.pack(side=tk.TOP, expand=True)
        title_left = tk.Label(title, text="AMAZE", font=TkElements.Title_1)
        title_left.place(relx=0.4, rely=0.5, anchor="center")
        title_right = tk.Label(title, text="gen", font=TkElements.Title_2)
        title_right.place(relx=0.7, rely=0.55, anchor="center")
        
    def set_generation_text(root: tk.Frame, pos: float) -> None:
        lbl = tk.Label(root, text="Ready to start?", font=TkElements.Header)
        lbl.place(relx=0.5, rely=pos, anchor="center")
        
    def set_solution_text(root: tk.Frame, pos: float) -> None:
        line_one = tk.Label(root, text="Finished Generating", font=TkElements.Header)
        line_one.place(relx=0.5, rely=pos, anchor="center")
        
        line_two = tk.Label(root, text="Ready to Solve?", font=TkElements.Subtext)
        line_two.place(relx=0.5, rely=pos+.08, anchor="center")
        
    def set_finish_text(root: tk.Frame, pos: float) -> None:
        lbl = tk.Label(root, text="Finished Solving", font=TkElements.Header)
        lbl.place(relx=0.5, rely=pos, anchor="center")
        
    def set_slider(root: tk.Frame, pos: float, event, timestep) -> None:
        # Add a slider to select our timestep
        lbl = tk.Label(root, text="Time Step (ms)", font=TkElements.Subtext)
        lbl.place(relx=0.5, rely=pos, anchor="center")
        
        # Add a slider to select our timestep
        slider = tk.Scale(
            root, from_=1, to=500, length=250,
            orient=tk.HORIZONTAL, 
            command=event, 
            variable=timestep
        )
        slider.set(timestep)
        slider.place(relx=0.5, rely=pos+.08, anchor="center")
        
    def set_generation_info(root: tk.Frame, pos: float, gen) -> None:
        # Display info about generation
        lbl_dim_head = tk.Label(root, text="Dimensions", font=TkElements.Header)
        lbl_dim_head.place(relx=0.5, rely=pos, anchor="center")
        lbl_dim = tk.Label(root, text=f"{gen.width}x{gen.height}", font=TkElements.Subtext)
        lbl_dim.place(relx=0.5, rely=pos+.2, anchor="center")
        
        lbl_alg_head = tk.Label(root, text="Algorithm", font=TkElements.Header)
        lbl_alg_head.place(relx=0.5, rely=pos+.4, anchor="center")
        lbl_alg = tk.Label(root, text=f"{gen.name()}", font=TkElements.Subtext)
        lbl_alg.place(relx=0.5, rely=pos+.6, anchor="center")
        
    def set_solution_info(root: tk.Frame, pos: float, solve) -> None:
        # Display info about generation
        lbl_dim_head = tk.Label(root, text="Dimensions", font=TkElements.Header)
        lbl_dim_head.place(relx=0.5, rely=pos, anchor="center")
        lbl_dim = tk.Label(root, text=f"{solve.width}x{solve.height}", font=TkElements.Subtext)
        lbl_dim.place(relx=0.5, rely=pos+.2, anchor="center")
        
        lbl_alg_head = tk.Label(root, text="Algorithm", font=TkElements.Header)
        lbl_alg_head.place(relx=0.5, rely=pos+.4, anchor="center")
        lbl_alg = tk.Label(root, text=f"{solve.name()}", font=TkElements.Subtext)
        lbl_alg.place(relx=0.5, rely=pos+.6, anchor="center")
        