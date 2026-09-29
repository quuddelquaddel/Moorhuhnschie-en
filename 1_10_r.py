import pygame     #Bibliotheken importieren; subprocess ruft das eigentliche Spiel auf

pygame.init()                                                               #das pygame-Modul wird initialisiert
screen=pygame.display.set_mode((850,250))                                           #ein leeres (noch farbloses) Feld der Größe 800 x 250 wird erstellt

font=pygame.font.Font(None, 38)                                                 #Schriftgröße des Textes


class DynamicText(object):
    def __init__(self, font, pos):
        self.font=font
        self._gen=text_generator(self.text)                     #Initialisierung, daß auf den Textgenerator zugegriffen wird
        self.pos=pos                                            #Initialisierung einer (Text-)Position

    def reset(self):                                            #fasst den Textgenerator (also Texterzeuger) und den Abschluss des Textzeigens zusammen
        self.done=False
        self.update()
   
message=DynamicText(font, (65,120))                                       #Position des Textes im schwarzen Feld

while True:                                             #while True ist IMMER erfüllt
    for event in pygame.event.get():
        if event.type==pygame.QUIT:                     #wenn man auf QUIT, also das Kreuz oben rechts, klickt
            break                                       #endet die immer erfüllte while TRUE Schleife und der ganze hiesige Programmabschnitt ist beendet, aber die 2. if-Anweisung wird noch gecheckt
        else:                                               #sofern der User nicht auf QUIT klickt
            screen.fill(pygame.color.Color('black'))        #ein leeres (jetzt schwarzes) Feld
        continue                                        #die while Schleife (s.o.) wird weitergemacht (praktisch das Gegenteil von break)
    break                                               #aber sobald der ganze Text durch ist, gibt es sehr wohl ein break auf der Ebene der for-Schleife (das andere break war innerhalb der for Schleife)=>while Schleife endet
    
#pygame.quit()                                           #wir brauchen pygame nicht mehr
