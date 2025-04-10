import os
import sys

from Draw.plot import Plot
from Maze.cell import Cell
from Maze.maze import Maze

mWidth = 0
mHeight = 0
mGen = 0
mSolve = 0

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
    "2.) Choose algorithm",
    "3.) Don't Panic"
]

generateAlgorithms = [
    "Chose one of the following algorithms",
    "1.) Wilsons"
]

solveAlgorithms = [
    "Choose one of the following algorithms",
    "1.) Depth First",
    "2.) Breadth First",
    "3.) Dijkstras",
]

def clearConsole():
    if sys.platform in ("linux", "darwin"):
        os.system("clear")
    elif sys.platform == "win32":
        os.system("cls")
    else:
        print("clearConsole unsupported on platform: " + sys.platform)
        exit(1)

def mainText():
    print(title)
    for s in instructions:
        print(s)
    print()

    if mWidth > 0 and mHeight > 0: 
        print(f"Dimensions: {mWidth}x{mHeight}")
        print()

    if mGen > 0:
        genName = generateAlgorithms[mGen]
        print(f"Generating: {genName[4:]}") 
        print
        
    if mSolve > 0:
        solveName = solveAlgorithms[mSolve]
        print(f"Solving: {solveName[4:]}")
        print()

def mainTextRe():
    clearConsole()
    mainText()

def get_width():
    global mWidth
    while True:
        tmpWidth = input("Enter a width for the generated maze...")
        try:
            mWidth = int(tmpWidth)
        except ValueError as e: 
            print(f"Error: {e}")
        
        if mWidth > 9 and mWidth < 101:
            break
        else: 
            print("Keep dimensions reasonable: valid input 10-100")

def get_height():
    global mHeight
    while True:
        tmpHeight = input("Enter a height for the generated maze...")
        try:
            mHeight = int(tmpHeight)
        except ValueError as e: 
            print(f"Error: {e}")
        
        if mHeight > 9 and mHeight < 101:
            break
        else: 
            print("Keep dimensions reasonable: valid input 10-100")

def get_gen():
    global mGen
    
    for a in generateAlgorithms:
        print(a)
        
    print()
        
    while True:
        tmpGen = input("Enter your selection...")
        try:
            mGen = int(tmpGen)
        except ValueError as e:
            print(f"Error: {e}")
        
        if mGen == 1:
            break
        else:
            print("Choose one of the available options: valid input 1")
            
def get_solve():
    global mSolve
    
    for a in solveAlgorithms:
        print(a)
    
    print()
        
    while True:
        tmpSolve = input("Enter your selection...")
        try:
            mSolve = int(tmpSolve)
        except ValueError as e:
            print(f"Error: {e}")
        
        if mSolve in (1,2,3):
            break
        else:
            print("Choose one of the available options: valid input 1-3")


clearConsole()

mainText()

get_width()

mainTextRe()

get_height()

mainTextRe()

get_gen()

mainTextRe()

get_solve ()

mainTextRe()

mainTextRe()

input("Press any key to generate and solve...")

maze = Maze(mWidth, mHeight)
cells = maze.generate_wilsons()

mazePlot = Plot(cells)
mazePlot.draw_grid()
