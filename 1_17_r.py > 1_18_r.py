import pygame                   #die Bibliothek pygame wird immer gebraucht
from pygame import mixer        #mixer sorgt dafür, dass Bildschirmereignisse (wie z.B. Bildschirmbewegungen) und Töne (wie z.B. Abspannmusik) GLEICHZEITIG kommen 
from pygame.locals import* 

pygame.init()                   #initialisiere Pygame Bibliothek

NACHRICHT="""Sie haben das Spiel
''Moorhuhn abschießen ''
gespielt!

Ich hoffe es hat Ihnen Spaß gemacht!
Bumm, bumm, peng, peng!

Wieviel haben Sie getroffen?
Welchen Score haben Sie erreicht?

Ceaucescu, der ehemalige Diktator
von Rumänien wäre sehr stolz auf Sie!
Er war leidenschaftlicher Jäger.

Ok, am Schluss wurde auch er
erschossen.

Aber nicht in der Luft, sondern am 
Boden.

Wer, weiß: Vielleicht schaffen Sie es 
bei Ihrer Schießkunst einmal zum
Diktator!

Wie heißt es so schön?:
"Moorhühner rauschen durch die Nacht
im wilden Schrei nach Norden.

Doch nicht alle haben es geschafft.
Man wollte sie ermorden!"

...na ja, nur so reimt es sich.

Laut Wikipedia wurde folgender Witz
zum besten gekürt: Zwei Jäger sind       
im Wald unterwegs, als einer von 
ihnen zusammenbricht. Er scheint 
nicht mehr zu atmen, und seine
Augen sind glasig. Der andere Typ
zückt sein Telefon, ruft den Notdienst
an und stößt hervor: ‚Mein Freund
ist tot! Was kann ich nur machen?‘
Darauf der Telefonist: ‚Beruhigen
Sie sich. Ich kann Ihnen helfen.
Zuerst sollten wir sicherstellen,
dass er tot ist.‘ Kurze Pause, dann
ein Schuss. Zurück am Telefon sagt
er: ‚OK, was jetzt?‘""" .split('\n')                      #'split'-Fkt: Text in Liste umwandeln; das Trennzeichen ('\n') ist der Zeilenneubeginn

class Credits:
    def __init__(self, bildschirm, liste):
        self.bildschirm=bildschirm                          #hier wird ein Bildschirm initialisiert/festgelegt
        self.liste=liste                                    #die Liste ist die Nachricht
        self.schriftgröße=50                                #hier wird die Schriftgröße festgelegt
        self.schriftfarbe=(255,255,255)                     #Schriftfarbe weiß
        self.Bildschirmmitte=self.bildschirm.height/2 +5    #wo ist die Schrift anzusetzen (in der Mitte)
        self.zeilenabstand=60                               #hier wird der Zeilenabstand festgelegt 
        self.timer=0.0
        self.delay=0                                        #keine Verzögerung, d.h. SOFORT den scrollenden Text anzeigen
        self.Bildschirmoberfläche()                         #Initialisierung der Bildschirmoberfläche

    def Text(self, Nachricht):
        font=pygame.font.SysFont('Arial',                   #Schriftart.....
                                 self.schriftgröße)         #....und Größe wird hier festgelegt
        text=font.render(Nachricht,                         #render=übertragen: Der lange obige Text (s.o.)
                         True,                              #ja, es wird etwas übertragen
                         self.schriftfarbe)                 #...mitsamt dessen Schriftfarbe
        rect=text.get_rect(center=(self.bildschirm.centerx, #wo ist der Text enzusiedeln ? In der Mitte
                                   self.bildschirm.centery+self.Bildschirmmitte))
        return text, rect                                   #letzten Endes wird der Text und das Bildschirmrechteck, auf gut Deutsch gesagt, der Bilschirm, übertragen

    def Bildschirmoberfläche(self):
        self.text=[]                                        #am Anfang ist das Array noch leer
        for i, zeile in enumerate(self.liste):
            l=self.Text(zeile)
            l[1].y+=i*self.zeilenabstand
            self.text.append(l)

    def update(self):                                       #hier wfdbdfird als Fkt letztendlich dafür gesorgt, dass der Text scrollt
        if pygame.time.get_ticks()-self.timer > self.delay: 
            self.timer = pygame.time.get_ticks()
            for text, rect in self.text:
                rect.y -=1                                  #bei +=1 geht der Text von oben nach unten und erscheint dann praktisch gar nicht

    def Übertragung(self, surf):
        for text, rect in self.text:
            surf.blit(text, rect)           #die blit-Fkt läßt uns das Bild verschieben

screen=pygame.display.set_mode((800,600))   #Bildschirmgröße
bildschirm=screen.get_rect()                #der Bildschirm an sich
clock=pygame.time.Clock()
running=True
cred=Credits(bildschirm,                    #hier wird auf die Klasse zugegriffen: Es wird ein Bildschirm erzeugt mitsamt dessen NACHRICHT (s.o.)
             NACHRICHT)
mixer.music.load("Abspannmusik.wav")        #hier wird die Abspannmusik geladen
mixer.music.play(1)                         #Musik wird genau 1x gespielt
while running:                              #diese Schleife ist immer wahr, weil running auf TRUE gesetzt wurde (s.o.) => Endlosschleife
    screen.fill((0,0,0))                    #Hintergrundfarbe (0,0,0) ist schwarz
    cred.update()                           #hier wird dafür gesorgt, daß der Text runterscrollt
    cred.Übertragung(screen)                #auf die NACHRICHT (siehe ganz oben) wird die Fkt "Übertragung" angewendet und auf dem Bildschirm gezeigt
    pygame.display.update()                 #der Bildschirm wird ständig geupdated
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:         #wenn der scrollende Text vorbei ist
            mixer.music.stop()              #eigentlich insofern überflüssig, als dass die Musik ohnehin nur 1x gespielt wird
            running=False                   #das Programm läuft nicht mehr
            pygame.quit()                   #alles ist beendet
