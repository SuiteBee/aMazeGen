import tkinter as tk
from Draw.kinterCell import KinterCell

class KinterPlot:
    def __init__(self, width, height, isAnimated):
        self.window = tk.Tk()
        self.canvas = None
        self.window.title("Maze Generator")
        
        self.isAnimated = isAnimated
        self.timeStep = 1
        
        self.width = width
        self.height = height
        self.aspect = width/height

        self.target_width = 1000
        self.target_height = 1000

        self.canvas_width = -1
        self.canvas_height = -1
        self.unit = -1 
        self.canvas_padding = 20
        self.__configure()

        self.edge_width = 1 if width + height > 100 else 2
        self.graph = self.__get_graph()
        self.queue = []
        
    def draw_multiple(self, group: list[tuple[tuple[int,int],tuple[str,str]]]):
        for step in group:
            address = step[0]
            instruction = step[1]
            self.__prepare_frame(address, instruction)
            
        self.window.after(self.timeStep, self.window.update())
        
    def draw_frame(self, address: tuple[int,int], instruction: tuple[str,str]):   
        self.__prepare_frame(address, instruction)
        self.window.after(self.timeStep, self.window.update())
        
    def __prepare_frame(self, address: tuple[int,int], instruction: tuple[str,str]):
        x = address[0]
        y = address[1]
        
        part = instruction[0]

        if part == "cell":
            color = instruction[1]
            self.graph[x][y].set_color(self.canvas, color)
        elif part == "border":
            direction = instruction[1]
            self.graph[x][y].remove_border(self.canvas, direction)

    def __configure(self):
        if self.target_width / self.target_height >= self.aspect:
            self.canvas_width = int(self.target_height * self.aspect)
            self.canvas_height = self.target_height

            self.unit = self.canvas_width / self.width 
        else:
            self.canvas_width = self.target_width
            self.canvas_height = int(self.target_width / self.aspect)

            self.unit = self.canvas_height / self.height
            
        self.canvas_width += (self.canvas_padding * 2)
        self.canvas_height += (self.canvas_padding * 2)

        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()
        
    def __get_graph(self):
        """Create a 2d list representation of our maze with KinterCells
        """
        
        tmp = [[0 for y in range(self.height)] for x in range(self.width)]
        
        for x in range(self.width):
            for y in range(self.height):
                origin = (x * self.unit, y * self.unit)
                opposite = (origin[0] + self.unit, origin[1] + self.unit)
                
                kCell = self.__generate_cell(origin, opposite, "black")
                tmp[x][y] = kCell
                
        return tmp

    def __adjust_point(self, point):
        x = point[0] + self.canvas_padding
        y = self.__reverse_coordinate(point[1] + self.canvas_padding)
        
        return (x,y)

    def __reverse_coordinate(self, yCoord: int) -> int:
        return self.canvas_height - yCoord

    def __generate_cell(self, point1, point2, color):
        x1,y1 = self.__adjust_point(point1)
        x2,y2 = self.__adjust_point(point2)
        id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        
        top = self.canvas.create_line(x1, y2, x2, y2, fill="black", width=self.edge_width)
        bottom = self.canvas.create_line(x1, y1, x2, y1, fill="black", width=self.edge_width)
        left = self.canvas.create_line(x1, y1, x1, y2, fill="black", width=self.edge_width)
        right = self.canvas.create_line(x2, y1, x2, y2, fill="black", width=self.edge_width)
        
        return KinterCell(id, top, bottom, left, right)