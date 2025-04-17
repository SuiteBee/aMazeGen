from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons
from Maze.Generate.ellers import Ellers

maze = None

width = 6
height = 6

#maze = Prims(width, height, True)
#maze = Wilsons(width, height, False)
maze = Ellers(width, height, True)

maze.generate()

