from Maze.cell import Cell
from Draw.plot import Plot
import random

class Animated:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.cells = [[Cell() for y in range(height)] for x in range(width)]
        self.visited = []
        self.unvisited = []
        self.path = []
        self.plotted = []
        
        # Possible Directions (Up), (Down), (Left), (Right)
        # Directions as x,y coordinates
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        
        self.plot = Plot(self.cells)
        
    def generate_wilsons(self):
        
        self.plot.live_plot()
        
        # Fill unvisited[] with all cells
        for x in range(self.width):
            for y in range(self.height):
                self.unvisited.append((x,y))
                
        # Add first point to the maze
        start = random.choice(self.unvisited)
        self.add_cell(start)
        self.plot.draw_single(self.cells[start[0]][start[1]], start[0], start[1], "white")
        
        # Loop until all cells are visited
        while len(self.unvisited) > 0:     
            # Choose next random point
            src = random.choice(self.unvisited)
            
            # Walk back to a point in the maze
            self.take_walk(src)
            
            # Mark all cells in our path as visited (i.e. add to maze)
            for i in range(len(self.path)):
                step = self.path[i]
                self.add_cell(step)
                self.plot.draw_single(self.cells[step[0]][step[1]], step[0], step[1], "white")
            
            # Cut a path in reverse (set borders)
            self.cut_path()
            
            for i in range(len(self.visited)):
                step = self.visited[i]
                if step not in self.plotted:
                    self.plotted.append(step)
                    self.plot.draw_single_border(self.cells[step[0]][step[1]], step[0], step[1])
                    
        self.plot.show()

    def add_cell(self, address):
        if address not in self.visited:
            self.visited.append(address)
            
        if address in self.unvisited:
            self.unvisited.remove(address)
            
        self.cells[address[0]][address[1]].visited = True

    # Walk from random point to point in maze
    def take_walk(self, src):
        # Add our start to the path
        self.path.append(src)
        
        # Get next cell to add to path
        current = self.get_next_cell(src)
        
        self.plot.draw_single(self.cells[current[0]][current[1]], current[0], current[1], "red")
        
        # Continue until we have reached the random point
        while current not in self.visited:
            # Loop Detected
            if current in self.path:
                #Remove loop from path and retry
                while current != self.path[-1]:
                    removed = self.path.pop()
                    self.plot.draw_single(self.cells[removed[0]][removed[1]], removed[0], removed[1], "black")
            # Path is valid continue from current
            else:
                self.path.append(current)
                self.plot.draw_single(self.cells[current[0]][current[1]], current[0], current[1], "red")
                
            # Get next cell to add to path
            current = self.get_next_cell(current)
            
        # Add our target to process wall removal
        self.path.append(current)
    
    # Set walls relative to path taken in reverse
    # i.e. open wall in path of travel
    def cut_path(self):
        tail = self.path.pop()
        
        while len(self.path) > 0:
            previous = self.path.pop()  
        
            # Get the direction we came from
            dir = self.get_direction(tail, previous)

            # Since we are traveling in reverse we can interpret this is as coming from [dir]
            if dir == 'down':
                self.cells[tail[0]][tail[1]].top = 0
                self.cells[previous[0]][previous[1]].bottom = 0
            elif dir == 'up':
                self.cells[tail[0]][tail[1]].bottom = 0
                self.cells[previous[0]][previous[1]].top = 0
            elif dir == 'left':
                self.cells[tail[0]][tail[1]].right = 0
                self.cells[previous[0]][previous[1]].left = 0
            elif dir == 'right':
                self.cells[tail[0]][tail[1]].left = 0
                self.cells[previous[0]][previous[1]].right = 0
            
            # Set tail to be the cell we just processed for next iteration
            if len(self.path) > 0:
                tail = previous
                
    def get_direction(self, tail, previous):       
        direction = tail[0] - previous[0], tail[1] - previous[1]
        index = self.directions.index(direction)

        if index == 0:
            return 'up'
        elif index == 1:
            return 'down'
        elif index == 2:
            return 'left'
        elif index == 3:
            return 'right'
         
    def get_next_cell(self, src):
        travel = random.choice(self.directions)
        
        nextCellX = src[0] + travel[0]
        nextCellY = src[1] + travel[1]
        
        if(nextCellX >= 0 and nextCellX < self.width and nextCellY >= 0 and nextCellY < self.height):
            return (nextCellX, nextCellY)
        else:
            return self.get_next_cell(src)