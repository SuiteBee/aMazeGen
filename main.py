from Maze.maze import Maze
from Maze.Generate.wilsons import Wilsons
from UI.userInterface import UserInterface

# Instantiate interface and make selections
options = UserInterface()
options.show()

# Pause before continuing
input("Press any key to generate and solve...")

maze = None

if options.mGen == 1:
    maze = Wilsons(options.width, options.height, False)

maze.generate()
