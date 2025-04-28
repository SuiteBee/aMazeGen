from Maze.Generate.prims import Prims
from Maze.Generate.wilsons import Wilsons
from Maze.Generate.ellers import Ellers

from Maze.Solve.dfs import DFS
from Maze.Solve.bfs import BFS
from Maze.Solve.best import Best
from Draw.tkController import TkController

maze = None

width = 100
height = 100

start = (0, height-1)
finish = (width-1, 0)

animate = False

output = TkController(width, height, animate)

#gen = Prims(output, width, height)
#gen = Wilsons(output, width, height)
gen = Ellers(output, width, height)

# Tell our drawing class we are ready to generate
output.begin_generation()

maze = gen.generate()

output.isAnimated = True
output.animator.isAnimated = True

while True:
    
    output.finish_generation()

    solution = BFS(output, maze)   
    solution.solve(start, finish)

    repeat = output.finish_solution()

    if repeat:
        solution.reset()
    else:
        exit()

