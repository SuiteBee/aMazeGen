from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
class Instruction(Enum):
    CELL = 1
    BORDER = 2
    TEXT = 3
    
class Border(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    
class Color(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    WHITE = "white"
    BLACK = "black"
    PINK = "pink"