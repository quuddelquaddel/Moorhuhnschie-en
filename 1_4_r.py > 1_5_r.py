from turtle import Screen, Turtle
import random 

SCHÜSSE = 20
GESCHWINDIGKEIT = 1
BREITE, HÖHE = 1280, 750

pygame.init()

class Bildmanager(Turtle):   					#Konfiguration des Bildes
    def __init__(self, breite, höhe): 			#Spezielle Turtle, hat die Aufgabe die Moorhuhn-GUI zu kontrollieren
        Turtle.__init__(self, visible=False)
        self.screen = Screen()
        self.screen.setup(breite, höhe)
        self.speed(0)
        self.penup()
        self.goto(-BREITE//2 + 50,               #die '+50' bewirken, daß die Schrift etwas ins Bild hineinkommt
                  -HÖHE//2 + 20)                 #die '+20' bewirken, daß die Schrift etwas ins Bild hineinkommt
        self.pencolor("yellow")                  #Schriftfarbe
        
    def schrift(self, txt):					     #Output Text im Graphik Fenster
        self.clear()
        self.write(txt, font=("Arial", 18, "bold"))

class Huhn(Turtle):
    def __init__(self, bilddatei, moorhuhnspiel):
        Turtle.__init__(self, shape=bilddatei)
        self.spiel = moorhuhnspiel
        self.penup()
        self.speed(0)
        self.onclick(self.getroffen)                            #wenn auf das Huhn draufgeklickt wurde, gilt es als 'getroffen'
        self.start_links()

    def start_links(self):
        self.hideturtle()                                        #zuerst sind die Hühner noch nicht da.....
        self.setpos(-BREITE//2-20,                              #das ist der Bereich, von wo aus die Hühner starten; '-20' bewirkt, daß sie etwas außerhalb vom Bild starten
                    random.randint(-HÖHE//3,
                                   HÖHE//3))
        self.vx = random.randint(6,11) * GESCHWINDIGKEIT        #'vx' ist die Geschwindigkeit in X-Richtung
        self.vy = random.randint(-3,3) * GESCHWINDIGKEIT        #'vy' ist die Geschwindigkeit in Y-Richtung
        self.getroffen = False
        self.tot = False
        self.ausdemspiel_links = False
        self.showturtle()                                         #.....jetzt sind die Hühner da

    def schritt_links_rechts(self):
        if self.tot:
            self.vy = self.vy - 0.5 * GESCHWINDIGKEIT           #hier fällt das angeschossene Huhn runter
        x, y = self.position()
        x = x + self.vx                                         #hier die X-Koordinate des herunterfallenden Huhns
        y = y + self.vy                                         #hier die Y-Koordinate des herunterfallenden Huhns. Bei 'self.vy**2' fallen die Hühner nach oben :P
        self.goto(x,y)
        if x > BREITE//2 + 20 or abs(y) > HÖHE//2 + 10:         #die '+20' bzw. die '+10' sorgen dafür, daß die Hühner immer etwas weiterfliegen als die Bildgröße=>Hühner sind aus dem Bild raus
            if self.spiel.schuss != SCHÜSSE:
                self.start_links()
            else:                                               #dieser Abschnitt sorgt dafür, daß die Hühner bei Spielende nicht weiterfliegen
                self.ausdemspiel_links = True
                
    def getroffen(self, x, y):
        if self.tot or self.spiel.schuss==SCHÜSSE: 		#"self.spiel.schuss==SCHÜSSE" bedeutet game over
            return
        self.tot = True
        self.getroffen = True
        self.spiel.score = self.spiel.score+1

class MoorhuhnSpiel (object):    #Kombiniert die Bestandteile des Moorhuhnspiels. Legt Spielablauf fest
    def __init__(self):						#Kombiniert Elemente des Moorhuhn Spiels.
        self.bild = bild= Bildmanager(BREITE, HÖHE) 		#erzeugt Grafik-Fenster
        bild.screen.bgpic("landschaft.gif")                  #'bgpic' ist eine Methode, um ein Hintergrundbild zu installieren
        bild.schrift("Leertaste drücken, um Spiel zu beginnen!")
        bild.screen.register_shape("huhn01.gif")                #'register_shape' bekommt einen Namen als Argument, der mit '.gif' endet=>dieser Name wird als Bilddatei aufgefaßt und diese....
        bild.screen.register_shape("huhn02.gif")                #....Bilddatei als Turtle shape registriert. Danach kann die Methode 'shape()' aufgerufen werden, um der Turtle diese Gestalt....

        self.huehner_links = [Huhn("huhn01.gif", self),
                              Huhn("huhn02.gif", self)]
        self.gameover = True                                    #jetzt kann ein neues Spiel beginnen
        bild.screen.onclick(self.schuss, 1)
        bild.screen.onkey(self.spiel, "space")                  #"onkey" heißt soviel wie: "Wenn eine Taste gedrückt wird", hier 'space', soll die Fkt 'spiel' aufgerufen werden
        bild.screen.listen()                                    #bewirkt, dass nach dem Tastendruck (s.o.) das Spiel auch tatsächlich anfängt
        bild.screen.getcanvas().config(cursor="circle") 	#get into Tkinter
        
    def spiel(self):
        if not self.gameover:
            return   						#altes Spiel läuft noch
        self.bild.schrift("SPIEL LÄUFT!")
        self.schuss = 0
        self.score = 0
        self.gameover = False
        for huhn in self.huehner_links:
            huhn.start_links()
        while not self.gameover:
            for huhn in self.huehner_links:
                huhn.schritt_links_rechts()
            gameover = self.schuss == SCHÜSSE
            for huhn in self.huehner_links:
                gameover = (gameover and huhn.ausdemspiel_links)
            self.gameover = gameover            
        
        self.bild.schrift ("Score: %1.2f" + " - Leertaste drücken!") # der Ausdruck '%1.2f' bedeutet 1 Vorkommastelle und 2 Nachkommastellen im Float System
           
    def schuss(self, x, y):
        if self.schuss == SCHÜSSE:
            return 						#es läuft kein Spiel, also kein Schuß
        self.schuss = self.schuss + 1
        for huhn in self.huehner_links: 
            if huhn.getroffen:
                huhn.getroffen = False
                break
        if self.schuss == SCHÜSSE:
            self.bild.schrift("SPIEL VORBEI!")
        else:        
            self.bild.schrift("Treffer/Schüsse: %d/%d" %(self.score, self.schuss))  #%d heißt: vz-behaftete Ganzzahl

def main():  							#Hauptfunktion
    MoorhuhnSpiel()
    return "EVENTLOOP"

if __name__ == "__main__":
    gnampf = main()
    print(gnampf)
    Screen().mainloop()                                         #prüft permanent, ob ein Event auftritt
    
