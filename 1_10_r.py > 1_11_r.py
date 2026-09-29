import pygame     #Bibliotheken importieren; subprocess ruft das eigentliche Spiel auf

pygame.init()                                                               #das pygame-Modul wird initialisiert
screen=pygame.display.set_mode((850,250))                                           #ein leeres (noch farbloses) Feld der Größe 800 x 250 wird erstellt

font=pygame.font.Font(None, 38)                                                 #Schriftgröße des Textes

pygame.time.set_timer(pygame.USEREVENT, 200)                                #die Zahl 200 gibt an, wie schnell der Text aufgeschrieben wird. Je größer die Zahl, umso langsamer

def text_generator(text):
    tmp= ' '                                                    #Leerzeichen
    for letter in text:                                         #gehe den ganzen Text durch
        tmp+=letter                                             #füge Zeichen (hier Buchstaben) hinzu
        if letter != ' ':                                       #wenn das Zeichen ungleich dem Leerzeichen ist 
            yield tmp                                           #füge Zeichen (hier Buchstaben) hinzu: der Witz hier ist, dass der Text selbst zwar Leerzeichen beinhaltet, selbst aber eine Konstante ist und damit künstlich keine Leerzeichen hat

class DynamicText(object):
    def __init__(self, font, text, pos):
        self.done=False                                         #die Aufgabenstellung, den Text darzustellen, ist noch nicht erfüllt
        self.font=font
        self.text=text                                          #Initialisierung eines Textes
        self._gen=text_generator(self.text)                     #Initialisierung, daß auf den Textgenerator zugegriffen wird
        self.pos=pos                                            #Initialisierung einer (Text-)Position
        self.update()                                           #update, d.h. gibt es noch etwas hinzuzufügen?

    def reset(self):                                            #fasst den Textgenerator (also Texterzeuger) und den Abschluss des Textzeigens zusammen
        self._gen=text_generator(self.text)
        self.done=False
        self.update()

    def update(self):
        if not self.done:                                       #sofern die Aufgabe, den Text zu zeigen, noch nicht vollständig abgeschlossen ist
            try:
                self.rendered=self.font.render(next(self._gen), True, (255,255,255))#Textfarbe (ich habe weiß genommen)
            except StopIteration:                               #sobald der Text fertiggezeigt ist und somit die Aufgabenstellung dieses Programmabschnitts erfüllt ist
                self.done=True                                  #....gilt die Aufgabenstellung dieses Programmabschnitts ab hier auch offiziell als erfüllt, d.h. die if Anweisungist erfüllt und stoppt
                
    def textverschiebung(self, screen):
        screen.blit(self.rendered, self.pos)                                #die blit Fkt lässt uns das Textbild verschieben
   
text=("Viel Spaß beim Computerspiel ''Moorhuhn abschießen'' !")     #der Text, den wir anzeigen wollen, bekommt hier eine eigene Konstante
message=DynamicText(font, text, (65,120)) 

while True:                                             #while True ist IMMER erfüllt
    for event in pygame.event.get():
        if event.type==pygame.QUIT:                     #wenn man auf QUIT, also das Kreuz oben rechts, klickt
            break                                       #endet die immer erfüllte while TRUE Schleife und der ganze hiesige Programmabschnitt ist beendet, aber die 2. if-Anweisung wird noch gecheckt
        if event.type==pygame.USEREVENT:                #falls der User ein Even (wie z.B. auf das Beenden-Kreuz zu klicken) angeklickt hat
            message.update()                            #wird auf die update Fkt zugegriffen, worin ja in der Subprocess Routine der Aufruf von "moorhuhn_2.py", also das richtige Spiel, schlummert
    else:                                               #sofern der User nicht auf QUIT klickt
        screen.fill(pygame.color.Color('black'))        #ein leeres (jetzt schwarzes) Feld
        message.textverschiebung(screen)                #die Funktion Textverschiebung wird aktiviert
        pygame.display.flip()                           #der Bildschirm (Display) zeigt immer neue Bilder, also im Klartext: Das Bild bleibt nicht stehen
        continue                                        #die while Schleife (s.o.) wird weitergemacht (praktisch das Gegenteil von break)
    break                                               #aber sobald der ganze Text durch ist, gibt es sehr wohl ein break auf der Ebene der for-Schleife (das andere break war innerhalb der for Schleife)=>while Schleife endet
    
#pygame.quit()                                           #wir brauchen pygame nicht mehr
