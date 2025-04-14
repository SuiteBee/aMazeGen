from Maze.maze import Maze
import random

class Wilsons(Maze):
    def __init__(self, width, height, isAnimated):
        super().__init__(width, height, isAnimated)
        
    def generate(self):
        
        self.plot.draw_start()
                
        # Add first point to the maze
        start = random.choice(self.unvisited)
        self.__add_cell(start)
        
        # Loop until all cells are visited
        while len(self.unvisited) > 0:     
            # Choose next random point
            src = random.choice(self.unvisited)
            
            # Walk back to a point in the maze
            self.__take_walk(src)
            
            # Mark all cells in our path as visited (i.e. add to maze)
            for i in range(len(self.path)):
                step = self.path[i]
                self.__add_cell(step)
            
            # Cut a path in reverse (set borders)
            self.__cut_path()
                    
        self.plot.draw_end()

    def __add_cell(self, address):
        if address not in self.visited:
            self.visited.append(address)
            
        if address in self.unvisited:
            self.unvisited.remove(address)
            
        self.cells[address[0]][address[1]].visited = True
        self.plot.set_color(address[0], address[1], "white")

    # Walk from random point to point in maze
    def __take_walk(self, src):
        # Add our start to the path
        self.path.append(src)
        
        # Get next cell to add to path
        current = self.__get_next_cell(src)
        
        # Mark our travel path red
        self.plot.set_color(current[0], current[1], "red")
        
        # Continue until we have reached the random point
        while current not in self.visited:
            # Loop Detected
            if current in self.path:
                # Remove loop from path and retry
                while current != self.path[-1]:
                    removed = self.path.pop()
                    self.plot.set_color(removed[0], removed[1], "black")
            else:
                # Path is valid continue from current
                self.path.append(current)
                
                # Mark our travel path red
                self.plot.set_color(current[0], current[1], "red")
                
            # Get next cell to add to path
            current = self.__get_next_cell(current)
            
        # Add our target to process wall removal
        self.path.append(current)
    
    # Set walls relative to path taken in reverse
    # i.e. open wall in path of travel
    def __cut_path(self):
        tail = self.path.pop()
        
        while len(self.path) > 0:
            previous = self.path.pop()  
        
            # Get the direction we came from
            dir = self.__get_direction(tail, previous)

            # Since we are traveling in reverse we can interpret this is as coming from [dir]
            if dir == 'down':
                # Remove walls from maze
                self.cells[tail[0]][tail[1]].top = 0
                self.cells[previous[0]][previous[1]].bottom = 0
                
                # Remove walls from plot
                self.plot.set_border(tail[0], tail[1], "top", False)
                self.plot.set_border(previous[0], previous[1], "bottom", False)
            elif dir == 'up':
                self.cells[tail[0]][tail[1]].bottom = 0
                self.cells[previous[0]][previous[1]].top = 0
                
                self.plot.set_border(tail[0], tail[1], "bottom", False)
                self.plot.set_border(previous[0], previous[1], "top", False)
            elif dir == 'left':
                self.cells[tail[0]][tail[1]].right = 0
                self.cells[previous[0]][previous[1]].left = 0
                
                self.plot.set_border(tail[0], tail[1], "right", False)
                self.plot.set_border(previous[0], previous[1], "left", False)
            elif dir == 'right':
                self.cells[tail[0]][tail[1]].left = 0
                self.cells[previous[0]][previous[1]].right = 0
                
                self.plot.set_border(tail[0], tail[1], "left", False)
                self.plot.set_border(previous[0], previous[1], "right", False)
            
            # Set tail to be the cell we just processed for next iteration
            if len(self.path) > 0:
                tail = previous
                
    def __get_direction(self, tail, previous):       
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
         
    def __get_next_cell(self, src):
        travel = random.choice(self.directions)
        
        nextCellX = src[0] + travel[0]
        nextCellY = src[1] + travel[1]
        
        # Check if the next cell x,y coordinates are within the maze
        if(nextCellX >= 0 and nextCellX < self.width and nextCellY >= 0 and nextCellY < self.height):
            return (nextCellX, nextCellY)
        else:
            return self.__get_next_cell(src)