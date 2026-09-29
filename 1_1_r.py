from turtle import Screen, Turtle
import random 

class Huhn(Turtle):
    pass

class MoorhuhnSpiel:    
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(640, 480)
        self.screen.clear()
        self.screen.bgpic("landschaft.gif")
        self.screen.register_shape("huhn01.gif")
        self.screen.register_shape("huhn02.gif")
        
if __name__ == "__main__":
    spiel = MoorhuhnSpiel()
    
