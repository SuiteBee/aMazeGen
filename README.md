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
+ Run the program from a command prompt with arguments to bypass the interface (mistakes will print the expected usage)
+ Perform either of the above from source

## Interface

Once the user has selected the parameters successfully, they are greeted with the TKinter GUI where they can select an animation timestep and click the button to begin

### The order of events are as follows

+ The program will generate the maze at the rate specified with colors to illustrate what is happening and when
+ The user can at any point change the timestep or pause the animation and continue
+ The program will halt at this point and wait for the user to trigger the solution
+ The solution will be animated again with options to change the timestep or pause
+ Once this step is complete the user can restart the solution or close the program

## Generation Algorithms

I chose these based on what I thought looked the most interesting to watch in action and the fact that they all generate "perfect" mazes

### Wilson's

This algorithm generates a maze by selecting an arbitrary cell and marking it visited (part of the maze). It then selects a second arbitrary cell and will randomly navigate (walk) the grid until it encounters this cell, if at any point it runs into its own path it will backtrack to that collision cell and continue. After it reaches the target it will carve a path (remove walls) from its origin. The cycle then repeats with another arbitrary unvisited cell until all cells are visited.

In the animation you can see that the random walks are colored red and the cells that are a part of the maze are colored white. This algorithm can be incredibly slow especially on larger mazes, but it is interesting to watch.

![wilsons](https://github.com/user-attachments/assets/92792734-2a17-4d71-92d3-ee6c74474a2c)

### Prim's 

The following algorithm is a little more efficient than the last. It starts with an arbitrary cell and is marked as visited (part of the maze), it will then create a "frontier" by adding the neighboring cells to a separate set (not yet part of the maze). The algorithm then chooses a random cell from the frontier and performs the same steps, expanding the frontier by adding the neighboring cells and repeating until all cells are visited.

In similar fashion, the cells that are a part of the maze are white and the frontier cells are colored red. The result looks akin to an explosion that grows from the starting point.

![prims](https://github.com/user-attachments/assets/501a0d12-3587-4685-a8d2-ee08f04cbcbd)

### Eller's

This one was more difficult to implement. Eller's algorithm starts at the top and works row by row keeping track of connected sets as it goes. For the first row, every cell belongs to its own set. For each subsequent row it will randomly remove vertical walls between cells if they do not belong to the same set. If a wall is removed, the two sets are merged into one. For that same row it will then randomly remove the bottom wall maintaining that each set has at least one exit downwards. The cells below where the wall was removed will be added to that set and for the next row, cells without a set will become new sets. This will continue with each row until the last, where instead of randomly removing vertical walls it will remove the wall if the cells belong to disjointed sets so that all cells in the final row will be a part of one singular set.

That is a lot to wrap your head around, but in its complexity are some benefits. This is the only algorithm that can generate endless mazes in linear time and even maintain its minimal memory requirements by only needing to keep track of the sets for the previous and current row. Trying to illustrate what is happening here is tricky, however I decided to color cells belonging to new sets red, cells that were an extension of a set pink and cells that are processed and completed white.

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
