from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons

maze = None

width = 30
height = 30

maze = Prims(width, height, False)
#maze = Wilsons(width, height, False)

maze.generate()
