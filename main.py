from Maze.Generate.wilsons import Wilsons
from Maze.Generate.prims import Prims
from Maze.Generate.ellers import Ellers

from UI.userInterface import UserInterface
from Draw.tkDraw import TkDraw

# Instantiate interface and make selections
options = UserInterface()
options.show()

# Pause before continuing
input("Press any key to open the GUI...")

# Creates a window to draw/animate our maze
graphic_output = TkDraw(options.width, options.height, options.mAnimate)

# Generation algorithm
factory = None
if options.mGen == 1:
    factory = Wilsons(graphic_output, options.width, options.height, options.mAnimate)
elif options.mGen == 2:
    factory = Prims(graphic_output, options.width, options.height, options.mAnimate)
elif options.mGen == 3:
    factory = Ellers(graphic_output, options.width, options.height, options.mAnimate)

# Tell our drawing class we are ready to generate
graphic_output.begin_generation()

# Generate method will return our maze as list[list[cell]]
maze = factory.generate()

# Tell our drawing class we have finished generating 
graphic_output.finish_generation()
