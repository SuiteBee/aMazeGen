from Maze.Generate.wilsons import Wilsons
from Maze.Generate.prims import Prims
from Maze.Generate.ellers import Ellers

from UI.userInterface import UserInterface

# Instantiate interface and make selections
options = UserInterface()
options.show()

# Pause before continuing
input("Press any key to generate and solve...")

maze = None

# Generation algorithm
if options.mGen == 1:
    maze = Wilsons(options.width, options.height, options.mAnimate)
elif options.mGen == 2:
    maze = Prims(options.width, options.height, options.mAnimate)
elif options.mGen == 3:
    maze = Ellers(options.width, options.height, options.mAnimate)

maze.generate()
