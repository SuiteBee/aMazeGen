from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons
from Maze.Generate.ellers import Ellers

maze = None

width = 10
height = 10

#maze = Prims(width, height, True)
#maze = Wilsons(width, height, False)
maze = Ellers(width, height, False)

maze.generate()

