# aMazeGen

> [!TIP]
> Scroll to the bottom for GIFS
 
A maze generator covering multiple algorithms for both generation and solution that employs TKinter to visualize them 

The primary goal of this project was to learn Python. To do this I decided to work with mazes and come up with a creative way to compare the methods of solving them

# Features

## Execution

There are a few methods of running this program

### User can

+ Run an executable file to open the guided text-based interface
+ Run the program from a command prompt with arguments to bypass the interface (mistakes will print the expected usage)
+ Perform either of the above from source

<details>
<summary><h3>Screenshots</h3></summary>

# Shell Interface

![Screenshot 2025-04-30 024910](https://github.com/user-attachments/assets/54901477-e6ed-47f9-ab4e-d1f588e1d3b6)

# Command line arguments

![Screenshot 2025-04-30 024851](https://github.com/user-attachments/assets/bd050271-4066-42fb-aa0a-6b11cd30036c)

# Asking for help

![Screenshot 2025-04-30 025255](https://github.com/user-attachments/assets/ce09b737-fda4-4d78-8d87-f668302aeba6)

</details>


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

### Prim's 

### Eller's

## Solution Algorithms

I selected these particular solutions because the third algorithm is a nice combination of the first two with the addition of a heuristic

### Depth First Search

### Breadth First Search

### Best First Search

# Review

Working with Python was a pleasant experience. I appreciated the simplicity of the syntax and the speed at which I could go from writing code to running my program. There was not a lot of setup involved. Packaging the app was also very streamlined and took next to no input from myself with PyInstaller. There seems to be limitless numbers of libraries and extensions available as well. You can choose which constructs if any you want to include from more robust languages like abstract classes or enums.

I started out planning to use MatPlotLib for the GUI and animation and got so far as to be running the animations with it. However it turned out to be much too slow due to how MPL manages its drawn plots and updates the changes. It would get exponentially slower around a grid size of 15x15. I tried many methods to get around it or speed MPL up to no avail. I ended up scrapping that code and rewriting the GUI with TKinter, which in hindsight was much more appropriate for this task. Now I can get up to a grid size of 500x500 with little to no slowdown.

The algorithms were all fun to implement and see executed in real time. Eller's was easily the most challenging. There is not a lot of documentation anywhere regarding how the algorithm works and its a difficult method to wrap your head around. This was part of the reason I chose it, but it did take some effort to get through.
