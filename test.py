from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons

maze = None

width = 25
height = 25

maze = Prims(width, height, True)
#maze = Wilsons(width, height, True)

maze.generate()
