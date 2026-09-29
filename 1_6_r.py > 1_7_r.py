from turtle import Screen, Turtle
import random, time, pygame, winsound, json, os
from pygame import mixer                             #der Mixer ist dafür da, daß WÄHREND etwas erscheint GLEICHZEITIG ein Geräusch ertönt (und nicht nacheinander)

try:
    import winsound                                             #Sound Wiedergabe Schnittstelle, bietet Zugriff auf die grundlegende Sound- Spielmaschinerie
    _SOUND = True
except:
    _SOUND = False
    print("KEIN TON!") 

SCHÜSSE = 20                                     #Es sind am Anfang 20 Schuss vorhanden
GESCHWINDIGKEIT = 1                              #es ist eine Geschwindigkeit vorhanden, die den Schwierigkeitsgrad immer schneller werdender Hühner symbolisiert
BREITE, HÖHE = 1280, 750                         #Höhe und Breite der Hintergrundbilder werden hier als feste Zahlen angegeben
TREFFER = "getroffen.wav"                           #der Ton, wenn ein Huhn getroffen wird, also Absturzgeräusch
DANEBEN = "daneben.wav"                             #der Ton, wenn ein Huhn nicht getroffen wird
GUT = "gameover.wav"                                #der Ton, wenn man mittelmäßig viele Hühner getroffen hat
APPLAUS = "applaus.wav"                             #der Ton eines Applauses, wenn man hinreichend viele Hühner getroffen hat
LEVEL=1
pygame.init()                                     #hier wird die Pygame Bibliothek initialisiert

# Sound
mixer.music.load("hintergrundmusik.wav")                        #lädt nur die Hintergrundmusik
mixer.music.play(-1)                                            #spielt tatsächlich die Hintergrundmusik ab; "-1" heißt: theoretisch endlos

class Bildmanager(Turtle):   					#Konfiguration des Bildes
    def __init__(self, breite, höhe): 			#Spezielle Turtle, hat die Aufgabe die Moorhuhn-GUI zu kontrollieren
        Turtle.__init__(self, visible=False)     #die Hühner sind am Anfang noch nicht zu sehen
        self.screen = Screen()                    #wir haben einen Bildschirm.........
        self.screen.setup(breite, höhe)            #.....der aus Höhe und Breite besteht (wie oben angegeben)
        self.speed(0)                             #das Aufschreiben der Schrift auf dem Bildschirm hat noch keine Geschwindigkeit
        self.penup()                             #es wird noch nichts aufgeschrieben
        self.goto(-BREITE//2 + 50,               #die '+50' bewirken, daß die Schrift etwas ins Bild hineinkommt
                  -HÖHE//2 + 20)                 #die '+20' bewirken, daß die Schrift etwas ins Bild hineinkommt
        self.pencolor("yellow")                  #Schriftfarbe
        
    def schrift(self, txt):					     #Output Text im Graphik Fenster
        self.clear()                             #am Anfang steht noch keine Schrift da
        self.write(txt, font=("Arial", 18, "bold")) #wenn aber eine Schrift dasteht, soll die eine fette Arial-Schrift der Schriftgröße 18 sein

class Huhn(Turtle):
    def __init__(self, bilddatei, moorhuhnspiel):
        Turtle.__init__(self, shape=bilddatei)
        self.spiel = moorhuhnspiel
        self.penup()                                             #die Hühner sind wie ein Stift anzusehen und jetzt sind noch keine Hühner zu sehen
        self.speed(0)                                         #die Hühner haben noch keine Geschwindigkeit
        self.onclick(self.getroffen)                            #wenn auf das Huhn draufgeklickt wurde, gilt es als 'getroffen'
        self.start_links()                                     #die Hühner starten am Anfang sowohl am Rand links.... 

    def start_links(self):                                     #alles was jetzt hier kommt, bezieht sich auf sie nach rechts fliegenden Hühner
        self.hideturtle()                                        #zuerst sind die Hühner noch nicht da.....
        self.setpos(-BREITE//2-20,                              #das ist der Bereich, von wo aus die Hühner starten; '-20' bewirkt, daß sie etwas außerhalb vom Bild starten
                    random.randint(-HÖHE//3,                     #irgendwo (per Zufallsgenerator) auf einer VERSCHIEDENEN vertikalen Höhe starten die Hühner
                                   HÖHE//3))
        self.vx = random.randint(6,11) * GESCHWINDIGKEIT        #'vx' ist die Geschwindigkeit in X-Richtung
        self.vy = random.randint(-3,3) * GESCHWINDIGKEIT        #'vy' ist die Geschwindigkeit in Y-Richtung
        self.getroffen = False                                 #noch sind die Hühner nicht getroffen.....
        self.tot = False                                         #...und wenn sie nicht getroffen sind, dann sind sie auch nicht tot
        self.ausdemspiel_links = False                             #...und wenn sie nicht tot sind, sind sie logischerweise auch nicht aus dem Spiel, sondern fliegen immer noch umher
        self.showturtle()                                         #.....jetzt sind die Hühner da

    def schritt_links_rechts(self):                             #hier lernen die Hühner fliegen
        global Strafpunkt_links_rechts                          #die Strafpunkte beziehen sich auf nicht abgeschossene und damit entkommene Hühner
        Strafpunkt_links_rechts=1   #Strafpunkt=1, weil wenn Strafpunkt=0 und alle Hühner abgeschossen würden und kein Huhn entkommt, unten durch 0 geteilt werden müßte. So wird durch 1 geteilt.
        if self.ausdemspiel_links:
            time.sleep(0.01)   
            return
        if self.tot:                                             #wenn ein Huhn angeschossen ist, ist es tot
            self.vy = self.vy - 0.5 * GESCHWINDIGKEIT           #hier fällt das angeschossene Huhn runter: Hier wird die Absturzbahn berechnet 
        x, y = self.position()
        x = x + self.vx                                         #hier die X-Koordinate des herunterfallenden Huhns
        y = y + self.vy                                         #hier die Y-Koordinate des herunterfallenden Huhns. Bei 'self.vy**2' fallen die Hühner nach oben :P
        self.goto(x,y)                                         #die (abgeschossenen) Hühner folgen ihrer Absturzbahn
        if x > BREITE//2 + 20 or abs(y) > HÖHE//2 + 10:         #die '+20' bzw. die '+10' sorgen dafür, daß die Hühner immer etwas weiterfliegen als die Bildgröße=>Hühner sind aus dem Bild raus
            Strafpunkt_links_rechts=Strafpunkt_links_rechts+1   #pro entkommenes (=nicht abgeschossenes) Huhn gibt es 1 Strafpunkt
            if self.spiel.schuss != SCHÜSSE:                     #sofern noch nicht alle Schüsse verballert sind....
                self.start_links()                             #....kommen von links immer neue Hühner hinzu
            else:                                               #dieser Abschnitt sorgt dafür, daß die Hühner bei Spielende nicht weiterfliegen
                self.ausdemspiel_links = True
                
    def getroffen(self, x, y):                             #Funktion der TRUE/False-Bedingungen, wenn ein Huhn getroffen wurde
        if self.tot or self.spiel.schuss==SCHÜSSE: 		#"self.spiel.schuss==SCHÜSSE" bedeutet game over
            return
        self.tot = True                                         #das (angeschossene ud damit abgeschossene) Huhn wird als tot deklariert
        self.getroffen = True                                 #das Huhn gilt als getroffen
        self.spiel.score = self.spiel.score+1             #der Spieler bekommt einen Punkt

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
        trefferrate = self.score/self.schuss                        #getroffene Hühner dividiert durch die Anzahl der Schüsse (Prozentrate)
        self.bild.schrift ("Score: %1.2f" + " - Leertaste drücken!") # der Ausdruck '%1.2f' bedeutet 1 Vorkommastelle und 2 Nachkommastellen im Float System
        if trefferrate >= 0.8:                                      #wenn man mindestens 80% der Hühner abgeschossen hat....
            self.klang(GUT)                                         #....ertönt ein YEAH-Ruf
        elif 0.5 <= trefferrate < 0.75:                             #wenn man zwischen 50% und 75% der Hühner abgeschossen hat... 
            self.klang(APPLAUS)                                     #ertönt ein Applaus
            
        global Punkte                                               #hier wird ausgerechnet welchen Score/Punktezahl insgesamt man erreicht hat
        Punkte=LEVEL*trefferrate
        
    def schuss(self, x, y):
        if self.schuss == SCHÜSSE:     #wenn alle Schüsse verballert sind
            return 						#es läuft kein Spiel, also kein Schuß
        self.schuss = self.schuss + 1     #wenn man schießt, wird die Anzahl der verballerten Schüsse (aus den anfangs 20 Stück) um 1 erhöht (bis man die 20 erreicht)
        klangdatei = DANEBEN             #hier wird einer Variable eine Sounddatei zugeordnet
        for huhn in self.huehner_links: #für die linken Hühner
            if huhn.getroffen:         #wenn ein linkes Huhn getroffen ist....
                klangdatei = TREFFER     #....soll die Treffer-Sounddatei erklingen
                huhn.getroffen = False
                break
        if self.schuss == SCHÜSSE:             #wenn alle Schüsse verballert sind....
            self.bild.schrift("SPIEL VORBEI!") #....erscheint der Schriftzug, dass das Spiel vorbei ist
        else:        
            self.bild.schrift("Treffer/Schüsse: %d/%d" %(self.score, self.schuss))  #%d heißt: vz-behaftete Ganzzahl
        self.klang(klangdatei)

    def klang(self, soundfile):
        winsound.PlaySound(soundfile, winsound.SND_ASYNC)   #der Befehl 'SND_ASYNC' sorgt dafür, daß das Abspielen des Klangs das Spiel nicht unterbricht, bzw. anhält 

def main():  							#Hauptfunktion
    MoorhuhnSpiel()
    return "EVENTLOOP"

if __name__ == "__main__":
    gnampf = main()
    print(gnampf)
    Screen().mainloop()                                         #prüft permanent, ob ein Event auftritt
    
mixer.music.stop()                                  #Hintergrundmusik stoppt
