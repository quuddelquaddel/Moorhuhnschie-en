from itertools import cycle
import tkinter as tk 

class App(tk.Tk):
    def __init__(self, image_files, x, y, Verzögerung):

        tk.Tk.__init__(self)                                        #Tkinter Element wird erzeugt

        self.geometry('+{}+{}'.format(x,y))                         #Initialisierung des Formats
        self.Verzögerung=Verzögerung

        self.pictures=cycle((tk.PhotoImage(file=image), image)      #der Vorgang startet immer wieder von Neuem
                            for image in image_files)
        self.picture_display=tk.Label(self)
        self.picture_display.pack()                                 #alle Bilder werden reingepackt

    def show_slides(self):
        img_object, img_name=next(self.pictures)                    #es wird immer in der Liste auf das nächste Bild zugegriffen
        self.picture_display.config(image=img_object)               #die Bilder sollen im Display gezeigt werden: Die Bilder sind Objekte

        self.title(img_name)
        self.after(self.Verzögerung, self.show_slides)

    def run(self):
        self.mainloop()                                             #prüft permanent, ob ein Event auftritt

Verzögerung=1500
image_files= ["huhn01.gif",
              "huhn03.gif",
              "huhn02.gif",
              "huhn04.gif"]
x=100
y=50
app=App(image_files, x, y, Verzögerung)                         #Zugriff auf die Klasse: huhn01.gif - huhn04.gif im Rahmen der Größe 100x50 und mit der Verzögerung des Zeigens von 1500
app.show_slides()                                               #in der App sollen die Bilder gezeigt werden: Zugriff auf die Fkt show_slides
app.run()                                                       #in der App sollen die Bilder unendlich oft gezeigt werden
