helpString = """
    Usage:
        arg[0]: width (10-100)
        arg[1]: height (10-100)
        arg[2]: generation method (1-3)
            1. Wilson's (slow)
            2. Prim's (linear)
            3. Eller's (fast)
        arg[3]: solution method (1-3)
            1. Depth First
            2. Breadth First
            3. Best First
        arg[4]: animation (y/n/yes/no)
    """
            
class NoInterface:
    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        
        self.mGen = 0
        self.mSolve = 0
        self.mAnimate = -1
        
    def process(self, args: list[str]) -> None:
        if args[0] in ("help", "usage"):
            print(helpString)
            exit()
        elif len(args) == 5:
            self.validate(args)
        else:
            print("Argument Mismatch: All arguments are required")
            print(helpString)
            exit()

    def validate(self, args: list[str]) -> None:
        success = True
        msg = []
        
        if str.isdigit(args[0]) and int(args[0]) >= 10 and int(args[0]) <= 100:
            self.width = int(args[0])
        else:
            success = False
            msg.append("arg[0]")
        
        if str.isdigit(args[1]) and int(args[1]) >= 10 and int(args[1]) <= 100:
            self.height = int(args[1])
        else:
            success = False
            msg.append("arg[1]")
        
        if str.isdigit(args[2]) and int(args[2]) > 0 and int(args[2]) <= 3:
            self.mGen = int(args[2])
        else:
            success = False
            msg.append("arg[2]")
            
        if str.isdigit(args[3]) and int(args[3]) > 0 and int(args[3]) <= 3:
            self.mSolve = int(args[3])
        else:
            success = False
            msg.append("arg[3]")
            
        if args[4].upper() in ("Y","YES","N","NO"):
            self.mAnimate = True if args[4].upper() in ("Y","YES") else False
        else:
            success = False
            msg.append("arg[4]")
            
        if not success:
            print(f"Validation Error: {msg}")
            print(helpString)
            exit()