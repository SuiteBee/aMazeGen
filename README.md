# aMazeGen

> [!TIP]
> Scroll to the bottom for GIFS
 
A perfect maze generator with the purpose of illustrating a few of the algorithms for both generating and solving them

The definition of a perfect maze is one in which any two cells will have only one path between them 

The primary goal of this project was to learn Python. Mazes have always fascinated me so to accomplish this task I decided to create this project

# Features

## Execution

There are a few methods of running this program

### User can

+ Run an executable file to open the guided text-based interface
+ Run the program from a terminal with arguments to bypass the interface (mistakes will print the expected usage)
+ Compile for non-windows platforms from source with PyInstaller

> [!NOTE]
> See release notes for details

## Interface

Once the user has entered the correct parameters, they are greeted with the TKinter GUI where they can select an animation timestep and click the button to begin

### The order of events are as follows

+ Maze is generated at the timestep specified with colored animations
+ User can change timestep or pause during generation
+ Wait for user input to begin solution
+ User can change timestep or pause during solution
+ User can restart the solution or close the program

## Generation Algorithms

I chose these based on what I thought looked the most interesting to watch in action and the fact that they all generate "perfect" mazes

### Wilson's

This algorithm can be incredibly slow especially on larger mazes for the first few iterations, but it is my personal favorite of the methods. It is also one of the few algorithms capable of generating completely unbiased maze.

Steps

1. Start with a random cell A
   - Add cell to maze (WHITE)
2. Choose another random unvisited cell B
3. Traverse "walk" the maze from cell B until A is reached
   - Random "steps" on walk are RED
   - If at any point this path encounters itself (loop), backtrack to this collision cell
5. Add "walk" path cells to the maze and carve path (remove walls)
6. Repeat from step 2. until all cells are visited

![wilsons](https://github.com/user-attachments/assets/92792734-2a17-4d71-92d3-ee6c74474a2c)

### Prim's 

The following algorithm is a little more efficient than the last. However it results in mazes with many short paths due to its generation technique. It is fun to watch, as it looks like a slow growing explosion from the starting point.

Steps

1. Start with a random cell A
   - Add cell to maze (WHITE)
2. Add cells neighboring A to "frontier" (RED)
3. Choose a random frontier cell B
   - Add frontier cell to maze
   - Carve path back to random cell that is part of the maze
4. Expand frontier from cell B
5. Rpeat from step 3. until all cells are visited

![prims](https://github.com/user-attachments/assets/501a0d12-3587-4685-a8d2-ee08f04cbcbd)

### Eller's

This is the most complex of the generation methods, but in its complexity are some benefits. This is the only algorithm that can generate endless mazes in linear time and even maintain its minimal memory requirements by only needing to keep track of the sets for the current and previous row.

Steps

1. Add each cell in the first row to its own set (RED)
2. Moving from left to right
   - Randomly remove vertical (right) walls of cells not a part of the same set
   - If a wall was removed, join the sets of cells on the left and right (WHITE)
3. Moving from left to right
   - Randomly remove horizontal (bottom) walls
   - If a cell is the only member of its set, remove the bottom wall
   - If a cell is the only member of its set with a bottom wall, remove this wall
   - If a wall was removed, join the cell below to the set above (PINK)
4. Move to the next row and add each cell not a part of an existing set to its own new set
5. Repeat from step 2 until the last row
6. Moving from left to right
   - Remove vertical (right) walls separating cells of different sets
   - If a wall was removed, join the sets of cells on the left and right
   - All cells in the bottom row should be a part of the same set


![ellers](https://github.com/user-attachments/assets/bb4c651a-6e11-495b-b59f-76ad523666fc)

## Solution Algorithms

I selected these particular solutions because the third algorithm is a nice combination of the first two with the addition of a heuristic

### Depth First Search

This algorithm operates in an unweighted graph by traversing as far as it can go by choosing random directions when encountering an intersection. When it gets stuck in a dead end, the algorithm will backtrack and continue at the last intersection with an unvisited neighbor. The travel path here is colored red and cells that were visited, then backtracked will be colored pink

![depth_first](https://github.com/user-attachments/assets/91e12dde-3538-4154-92c2-4343979c6410)

### Breadth First Search

BFS operates much like Prim's in that it will expand from a starting point. This algorithm will expand in every direction that contains an unvisited cell until an exit is reached. For this animation I colored the visited cells pink and the "heads" of the travel paths red.

![breadth_first](https://github.com/user-attachments/assets/e1fc12a4-9446-4ce4-951e-4b9f7b0d5295)

### Best First Search

The final solution algorithm operates a little like both of the previous methods. It has a singular travel path like DFS, but can branch off in another direction like BFS. The determination of where it branches off is a heuristic based on cell distance from the exit. This algorithm starts by calculating the distance mentioned before of the current cells neighbors, then choosing the closest cell. It will do this in a continuous path until one of the previous encountered neighbors is closer than the current cells neighbors. It will then branch off and continue from that cell and repeat until the exit is reached. The current cell is colored red, the measured neighboring cells are colored yellow and visited cells are marked pink.

![best_first](https://github.com/user-attachments/assets/a07c0948-c9a7-4c6c-9019-9a6e5ed014ea)

# Scale

This program can handle mazes of many sizes if the processing power is available, I decided to cap the width/height at a maximum of 500 with a minimum of 3. The program will lag a bit during startup at higher bounds due to the increased initialization that has to occur. I also setup the GUI so that it will scale the UI and cells to fit in a window that is 70% of the screen size its running on.

![large_prims](https://github.com/user-attachments/assets/fe8c0932-d10c-4184-bc1b-6338ff187390)

![large_best](https://github.com/user-attachments/assets/48808ac6-ea79-4c69-965e-aa7b25f4d2f6)

# Asymmetric Dimensions

The app will also handle asymmetric sizes and take into account the aspect of the dimensions provided to size the UI and cells accordingly

![tall](https://github.com/user-attachments/assets/f3b26872-1acd-49df-b87a-175b307a9caf)


# Review

Working with Python was a pleasant experience. I appreciated the simplicity of the syntax and the speed at which I could go from writing code to running my program. There was not a lot of setup involved. Packaging the app was also very streamlined and took next to no input from myself with PyInstaller. There seems to be limitless numbers of libraries and extensions available as well. You can choose which constructs if any you want to include from more robust languages like abstract classes or enums.

I started out planning to use MatPlotLib for the GUI and animation and got so far as to be running the animations with it. However it turned out to be much too slow due to how MPL manages its drawn plots and updates the changes. It would get exponentially slower around a grid size of 15x15. I tried many methods to get around it or speed MPL up to no avail. I ended up scrapping that code and rewriting the GUI with TKinter, which in hindsight was much more appropriate for this task. Now I can get up to a grid size of 500x500 with little to no slowdown.

The algorithms were all fun to implement and see executed in real time. Eller's was easily the most challenging. There is not a lot of documentation anywhere regarding how the algorithm works and its a difficult method to wrap your head around. This was part of the reason I chose it, but it did take some effort to get through.
