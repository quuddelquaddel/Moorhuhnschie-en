from turtle import Screen, Turtle
import random 

class Huhn(Turtle):
    def __init__(self, bilddatei):
        Turtle.__init__(self, shape=bilddatei)
        self.hideturtle()
        self.penup()
        self.speed(0)

    def zumstart_links(self):
        self.hideturtle()
        self.setpos(-340, random.randint(-120, 120))
        self.vx = random.randint(6,11) 
        self.vy = random.randint(-3,3) 
        self.showturtle()
        self.tot = False

    def schritt_links_rechts(self):
        x, y = self.position()
        x = x + self.vx
        y = y + self.vy
        self.goto(x,y)

    def raus_nach_rechts(self):
        x, y = self.position()
        return x > 340 or abs(y) > 250

class MoorhuhnSpiel:    #Kombiniert die Bestandteile des Moorhuhnspiels. Legt Spielablauf fest
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(640, 480)
        self.screen.clear()
        self.screen.title("Moorhuhnspiel")
        self.screen.bgpic("landschaft.gif")
        self.screen.register_shape("huhn01.gif")
        self.screen.register_shape("huhn02.gif")

        # Der Schreib-Gehilfe
        self.schreiber = Turtle(visible=False)
        self.schreiber.speed(0)
        self.schreiber.penup()
        self.schreiber.goto(-290, -220)
        self.schreiber.pencolor("yellow")
        # Die Moorhühner
        self.huehner_links = (Huhn("huhn01.gif"),
                              Huhn("huhn02.gif"))

    def melde(self, txt):
        self.schreiber.clear()
        self.schreiber.write(txt, font=("Arial", 18, "bold"))

    def spiel(self):
        # Initialisierung
        self.screen.onkeypress(None, "space")
        self.melde("SPIEL LÄUFT!")
        self.schuesse = 0
        for huhn in self.huehner_links:
            huhn.zumstart_links()

        # Ausführung
        while self.schuesse < 5:  # SCHUESSE:
            for huhn in self.huehner_links:
                huhn.schritt_links_rechts()
                if huhn.raus_nach_rechts():
                    huhn.zumstart_links()
        self.screen.onclick(None)

        # Abschluss und Ergebnis
        self.screen.onkeypress(self.spiel, "space")
        self.melde("DAS SPIEL IST AUS! - Leertaste!!!")

    def run(self):
        self.melde("Start mit Leertaste!")
        self.screen.onkeypress(self.spiel, "space")
        self.screen.listen()
        
if __name__ == "__main__":
    spiel = MoorhuhnSpiel()
    spiel.run()
