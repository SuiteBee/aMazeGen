from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons
from Maze.Generate.ellers import Ellers

maze = None

width = 25
height = 25

#maze = Prims(width, height, False)
#maze = Wilsons(width, height, False)
maze = Ellers(width, height, True)

maze.generate()

