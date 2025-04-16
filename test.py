from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons

maze = None

width = 50
height = 50

maze = Prims(width, height, True)
#maze = Wilsons(width, height, True)

maze.generate()
