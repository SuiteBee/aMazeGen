from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons
from Maze.Generate.ellers import Ellers

from Maze.Solve.dfs import DFS
from Maze.Solve.bfs import BFS
from Draw.tkController import TkController

maze = None

width = 10
height = 10

start = (0, height-1)
finish = (width-1, 0)

animate = True

output = TkController(width, height, animate)

#gen = Prims(output, width, height)
#gen = Wilsons(output, width, height)
gen = Ellers(output, width, height)

# Tell our drawing class we are ready to generate
output.begin_generation()

maze = gen.generate()

output.finish_generation()

solution = DFS(output, maze)

solution.solve(start, finish)

output.finish_solution()

