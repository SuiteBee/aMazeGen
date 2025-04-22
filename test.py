from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons
from Maze.Generate.ellers import Ellers
from Draw.tkDraw import TkDraw

maze = None

width = 10
height = 10
animate = False

output = TkDraw(width, height, animate)

#maze = Prims(output, width, height)
#maze = Wilsons(output, width, height)
maze = Ellers(output, width, height)

# Tell our drawing class we are ready to generate
output.begin_generation()

maze.generate()

output.finish_generation()