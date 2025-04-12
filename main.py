from Draw.plot import Plot
from Maze.maze import Maze
from Maze.animated import Animated
from UI.interface import Interface

# Instantiate interface and make selections
options = Interface()
options.show()

# Pause before continuing
input("Press any key to generate and solve...")

maze = Animated(options.width, options.height)
cells = maze.generate_wilsons()

#maze = Maze(options.width, options.height)
#cells = maze.generate_wilsons()

#mazePlot = Plot(cells)
#mazePlot.draw()
