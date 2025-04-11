import os
import sys

title = """
███╗   ███╗ █████╗ ███████╗███████╗     ██████╗ ███████╗███╗   ██╗
████╗ ████║██╔══██╗╚══███╔╝██╔════╝    ██╔════╝ ██╔════╝████╗  ██║
██╔████╔██║███████║  ███╔╝ █████╗      ██║  ███╗█████╗  ██╔██╗ ██║
██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝      ██║   ██║██╔══╝  ██║╚██╗██║
██║ ╚═╝ ██║██║  ██║███████╗███████╗    ╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝
"""

instructions = [
    "Instructions",
    "1.) Enter maze dimensions",
    "2.) Choose algorithm to generate",
    "3.) Choose method to solve",
    "4.) Don't Panic"
]

generateAlgorithms = [
    "Chose one of the following algorithms",
    "1.) Wilsons",
    "2.) Prims",
    "3.) Kruskal or Aldous-Broder"
]

solveAlgorithms = [
    "Choose one of the following algorithms",
    "1.) Depth First",
    "2.) Breadth First",
    "3.) A* or Tremaux"
]

class Interface:
    def __init__(self):
        self.width = 0
        self.height = 0
        
        self.mGen = 0
        self.mSolve = 0
        
    # Main UI loop
    def show(self):

        self.__reset()
        self.__instructions()
        
        # Loop until we have all necessary info
        while self.__selection_required():
            self.__reset()
            
            if self.width == 0:
                self.width = self.__get_width()
            elif self.height == 0:
                self.height = self.__get_height()
            elif self.mGen == 0:
                self.mGen = self.__get_gen()
            elif self.mSolve == 0:
                self.mSolve = self.__get_solve()
                
        self.__reset()
        self.__show_selections()
        
    def __reset(self):
        self.__clear_console()
        print(title)
        print()
        
    def __instructions(self):
        for s in instructions:
            print(s)
        print()
        
        input("Press any key to continue...")
        
    def __show_selections(self):
        print(f"Dimensions: {self.width}x{self.height}")
        print(f"Generating: {self.__generate_name()}") 
        print(f"Solving: {self.__solution_name()}")
        print()
        
    def __get_width(self):
        while True:
            tmpWidth = input("Enter a width for the generated maze: ")
            try:
                tmpWidth = int(tmpWidth)
            except ValueError as e: 
                print(f"Error: {e}")
            
            if tmpWidth > 9 and tmpWidth < 101:
                return tmpWidth
            else: 
                print("Keep dimensions reasonable: valid input 10-100")

    def __get_height(self):
        while True:
            tmpHeight = input("Enter a height for the generated maze: ")
            try:
                tmpHeight = int(tmpHeight)
            except ValueError as e: 
                print(f"Error: {e}")
            
            if tmpHeight > 9 and tmpHeight < 101:
                return tmpHeight
            else: 
                print("Keep dimensions reasonable: valid input 10-100")

    def __get_gen(self):
        for a in generateAlgorithms:
            print(a)       
        print()
            
        while True:
            tmpGen = input("Enter your selection: ")
            try:
                tmpGen = int(tmpGen)
            except ValueError as e:
                print(f"Error: {e}")
            
            if tmpGen == 1:
                return tmpGen
            else:
                print("Choose one of the available options: valid input 1")
            
    def __get_solve(self):
        for a in solveAlgorithms:
            print(a)
        
        print()
            
        while True:
            tmpSolve = input("Enter your selection: ")
            try:
                tmpSolve = int(tmpSolve)
            except ValueError as e:
                print(f"Error: {e}")
            
            if tmpSolve in (1,2,3):
                return tmpSolve
            else:
                print("Choose one of the available options: valid input 1-3")
            
    def __selection_required(self):
        return self.width == 0 or self.height == 0 or self.mGen == 0 or self.mSolve == 0
        
    def __generate_name(self):
        return generateAlgorithms[self.mGen][4:]
    
    def __solution_name(self):
        return solveAlgorithms[self.mSolve][4:]
    
    def __clear_console(self):
        if sys.platform in ("linux", "darwin"):
            os.system("clear")
        elif sys.platform == "win32":
            os.system("cls")
        else:
            print("clear_console unsupported on platform: " + sys.platform)
            exit(1)