import sys

from Maze.Generate.wilsons import Wilsons
from Maze.Generate.prims import Prims
from Maze.Generate.ellers import Ellers

from Maze.Solve.dfs import DFS
from Maze.Solve.bfs import BFS
from Maze.Solve.best import Best

from Interface.noInterface import NoInterface
from Interface.shellInterface import ShellInterface
from Interface.GUI.tkController import TkController

# Determine whether to open the interactive shell or run with command line arguments
if len(sys.argv) - 1 > 0:
    # Arugments given, process arguments
    options = NoInterface()
    
    # Pass all arguments except script name
    options.process(sys.argv[1:])
    
else:
    # Instantiate interface and make selections
    options = ShellInterface()
    
    # Interactive shell
    options.show()
    
    # Pause before continuing
    input("Press any key to open the GUI...")

# Creates a window to draw/animate our maze
gui = TkController(options.width, options.height, options.mAnimate)

# Generation algorithm
architect = None
if options.mGen == 1:
    architect = Wilsons(gui, options.width, options.height)
elif options.mGen == 2:
    architect = Prims(gui, options.width, options.height)
elif options.mGen == 3:
    architect = Ellers(gui, options.width, options.height)

# Handle application window closing
try:
    
    # Tell our GUI we are ready to generate
    gui.begin_generation()

    # Generate method will return our maze as list[list[cell]]
    maze = architect.generate()

    # Set our start and end coordinates
    start = (0, options.height-1)
    finish = (options.width-1, 0)

    # Begin solution loop, will re-run solution until [close] button is pressed
    while True:
    # Tell our GUI we have finished generating 
        gui.finish_generation()

        # Solution algorithm
        pathfinder = None
        if options.mSolve == 1:
            pathfinder = DFS(gui, maze)
        elif options.mSolve == 2:
            pathfinder = BFS(gui, maze)
        elif options.mSolve == 3:
            pathfinder = Best(gui, maze) 
        
        # Solve method will reutnr our solution as list[Cell]
        solution = pathfinder.solve(start, finish)

        # Tell our gui we have solved the maze
        repeat = gui.finish_solution()

        # Button press from above will determine if we solve again
        if repeat:
            pathfinder.reset()
        else:
            sys.exit()

except:
    sys.exit()