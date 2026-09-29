from turtle import Screen, Turtle
import random, time, pygame, winsound, json, os
from pygame import mixer                             #der Mixer ist dafür da, daß WÄHREND etwas erscheint GLEICHZEITIG ein Geräusch ertönt (und nicht nacheinander)
from moorhuhn_2 import Level

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
        self.start_rechts()                                     #.....als auch rechts

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

    #############################################################
    def start_rechts(self):                                     #alles was jetzt hier kommt, bezieht sich auf sie nach links fliegenden Hühner         
        self.hideturtle()                                       #zuerst sind die Hühner noch nicht da.....          
        self.setpos(BREITE//2+20,                               #das ist der Bereich, von wo aus die Hühner starten ; '+20' bewirkt, daß sie etwas außerhalb vom Bild starten
                    random.randint(-HÖHE//3,                    #irgendwo (per Zufallsgenerator) auf einer VERSCHIEDENEN vertikalen Höhe starten die Hühne
                                   HÖHE//3))                    #
        self.vx = random.randint(6,11) * GESCHWINDIGKEIT        #'vx' ist die Geschwindigkeit in X-Richtung         
        self.vy = random.randint(-3,3) * GESCHWINDIGKEIT        #'vy' ist die Geschwindigkeit in Y-Richtung         
        self.getroffen = False                                  #noch sind die Hühner nicht getroffen...
        self.tot = False                                        #...und wenn sie nicht getroffen sind, dann sind sie auch nicht tot
        self.ausdemspiel_rechts = False                         #...und wenn sie nicht tot sind, sind sie logischerweise auch nicht aus dem Spiel, sondern fliegen immer noch umher
        self.showturtle()                                       #.....jetzt sind die Hühner da
                                                                #
    def schritt_rechts_links(self):                             #hier lernen die Hühner fliegen
        global Strafpunkt_rechts_links                          #die Strafpunkte beziehen sich auf nicht abgeschossene und damit entkommene Hühner
        Strafpunkt_rechts_links=1                               #siehe Erklärung oben, sonst zu langer Kommentar
        if self.ausdemspiel_rechts:                             #
            time.sleep(0.01)                                    #
            return                                              #
        if self.tot:                                            #wenn ein Huhn angeschossen ist, ist es tot
            self.vy = self.vy + 0.5 * GESCHWINDIGKEIT           #hier fällt das angeschossene Huhn runter           
        x, y = self.position()                                  #Absturzbahhn hat eine X und eine Y Koordinate                                                    
        x = x - self.vx                                         #hier die X-Koordinate des herunterfallenden Huhns  
        y = y - self.vy                                         #hier die Y-Koordinate des herunterfallenden Huhns  
        self.goto(x,y)                                          #die (abgeschossenen) Hühner folgen ihrer Absturzbahn
        if x < -BREITE//2 - 20 or abs(y) > HÖHE//2 + 10:        #die '-20' bzw. die '+10' sorgen dafür, daß die Hühner immer etwas weiterfliegen als die Bildgröße=>Hühner sind aus dem Bild raus
            Strafpunkt_rechts_links=Strafpunkt_rechts_links+1   #pro entkommenes (=nicht abgeschossenes) Huhn gibt es 1 Strafpunkt
            if self.spiel.schuss != SCHÜSSE:                    #sofern noch nicht alle Schüsse verballert sind....
                self.start_rechts()                             #....kommen von links immer neue Hühner hinzu
            else:                                               #dieser Abschnitt sorgt dafür, daß die Hühner bei Spielende nicht weiterfliegen
                self.ausdemspiel_rechts = True                  #
    #############################################################
    
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
        #########################################################
        bild.screen.register_shape("huhn03.gif")                #....zu verleihen. Bilddateien auf '*.gif' endend können jede Gestalt und alle Methoden (z.B. 'left' & 'right') ausführen.
        bild.screen.register_shape("huhn04.gif")                #
        #########################################################
        self.huehner_links = [Huhn("huhn01.gif", self),
                              Huhn("huhn02.gif", self)]
        #####################################################
        self.huehner_rechts = [Huhn("huhn03.gif", self),    #und hier die rechts startenden Hühner
                               Huhn("huhn04.gif", self)]    #
        #####################################################
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
        #####################################
        for huhn in self.huehner_rechts:    #und 1:1 dasselbe für die rechts fliegenden Hühner
            huhn.start_rechts()             #
        #####################################
        while not self.gameover:
            for huhn in self.huehner_links:
                huhn.schritt_links_rechts()
            #####################################
            for huhn in self.huehner_rechts:    #...fliegen die initial rechts sich befindlichen Hühner                   
                huhn.schritt_rechts_links()     #....nach  links
            #####################################
            gameover = self.schuss == SCHÜSSE
            for huhn in self.huehner_links:
                gameover = (gameover and huhn.ausdemspiel_links)
            #########################################################
            for huhn in self.huehner_rechts:                        #für die rechten Hühner, die nach rechts fliegen....
                gameover = (gameover and huhn.ausdemspiel_rechts)   #...ist der Gameover Status dann erreicht, wenn alle Schüsse verballert sind und alle nach links fliegenden Hühner aus dem Bild sind
            #########################################################
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
        #########################################
        for huhn in self.huehner_rechts:        #hier der obige Kladderadatsch nochmal für die rechten Hühner (die also nach links fliegen)
            if huhn.getroffen:                  #
                klangdatei = TREFFER            #
                huhn.getroffen = False          #
                break                           #
        #########################################
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

        #############################################################################  #
        #                                                                           # ##
        #       Hier wírd eine Highscoreliste der Top 3 erstellt und verwaltet      ###############################################################
        #                                                                           # ##
        #############################################################################  #

def Schnellfkt_Neueintrag():
    Name=input("Geben Sie Ihren Namen ein! ")
    Neueintrag=[]
    Neueintrag.append(Punkte)
    Neueintrag_Namenseintrag=[]
    Neueintrag_Namenseintrag.append(Name)
    Neueintrag.append(Neueintrag_Namenseintrag)
    Highscores.append(Neueintrag)
    Highscores.sort(reverse=True)
    
if Punkte>0:                                        #man sollte zumindestens etwas getroffen haben, um in die Bestenliste zu kommen
    if os.path.exists("Bestenliste.json"):          #falls die Datei der Bestenliste bereits schon existiert
        filename = 'Bestenliste.json'
        with open(filename) as file_object:
            Highscores = json.load(file_object)     #hier wird die - bereits bestehende(!) - Highscoreliste geladen
        if len(Highscores) < 3:                     #hier wird dafür gesorgt, daß ein Highscore-Array der Länge 3 entsteht
            for i in range(len(Highscores)):
                if Highscores[i][0]==Punkte:        #die Punkte sind gleich groß wie ein bereits existierender Eintrag
                    Name=input("Geben Sie Ihren Namen ein! ")
                    Highscores[i][1].append(Name)   #nur der neue Name wird (zu dem alten, bereits bestehenden) hinzufegügt
                    break                           #die for-Schleife wird ab dem Zeitpunkt abgebrochen, ab dem irgendetwas Neues ins Array "Bestenliste" eingetragen wurde
                else:                               #die Punkte sind zueinander verschieden
                    Schnellfkt_Neueintrag()
                    filename= 'Bestenliste.json'                
                    break
        elif Punkte < Highscores[-1][0]:            #ab hier HAT das Highscore-Array bereits schon die Länge 3
            print("Schade! Damit haben Sie es leider nicht in die Top 3 geschafft!")
        else:                                       #der Spieler hat es zum 1x in die Highscoreliste geschafft
            for i in range(len(Highscores)):
                if Highscores[i][0] < Punkte:       #größerer Wert als der kleinste vorkommende Wert gefunden => der letzte (kleinste) Wert des Arrays fliegt raus
                    Schnellfkt_Neueintrag()         #ab hier wird die bereits bestehende Liste sortiert (aber noch nicht gespeichert)<-Sortieren ist für die Highscoreliste wichtig!
                    del(Highscores[-1])             #der letzte kleinste Wert ganz rechts im Array wird gelöscht, damit die Highscores noch immer die Top 3 repräsentieren
                    break
                if Highscores[i][0]==Punkte:        #gleichgroßer Wert gefunden
                    Name=input("Geben Sie Ihren Namen ein! ")
                    Highscores[i][1].append(Name)   #nur der neue Name wird (zu dem alten, bereits bestehenden) hinzufegügt
                    break
        filename= 'Bestenliste.json'
        with open(filename, 'w') as file_object:            #ab hier wird auch gespeichert
            json.dump(Highscores, file_object)
        with open(filename) as file_object:             #ab hier wird die bisherige Bestenliste in der Python Shell Zeile für Zeile gedruckt
            bisherige_Bestenliste=json.load(file_object)    #....erst laden
        for i in bisherige_Bestenliste:                     #....dann drucken
            print(i)
    else:                                           #falls die Datei der Bestenliste noch nicht existiert, ist dieser else-Block für die Erstellung dieser neuen Datei zuständig
        Highscores=[]                               #hier wird eine NEUE Highscoreliste erstellt
        Schnellfkt_Neueintrag()               
        filename= 'Bestenliste.json'                #...und der neuen Datei Ihren Namen gegeben
        with open(filename, 'w') as file_object:    #ab hier wird auch gespeichert
            json.dump(Highscores, file_object)
        with open(filename) as file_object:         #ab hier wird die neue, initiale Bestenliste zum 1x (und mit dem 1.Eintrag) in die Python Shell geladen....
            bisherige_Bestenliste=json.load(file_object)
        print(bisherige_Bestenliste)                #....und gedruckt
else:                                               #das ist der Fall, daß alle Schüsse danebengingen
    print("Sie haben kein einziges Moorhuhn abgeschossen!" )
