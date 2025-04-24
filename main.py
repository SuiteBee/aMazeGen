from Maze.Generate.wilsons import Wilsons
from Maze.Generate.prims import Prims
from Maze.Generate.ellers import Ellers

from UI.userInterface import UserInterface
from Draw.tkController import TkController

# Instantiate interface and make selections
options = UserInterface()
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

# Tell our GUI we are ready to generate
gui.begin_generation()

# Generate method will return our maze as list[list[cell]]
maze = architect.generate()

# Tell our GUI we have finished generating 
gui.finish_generation()
