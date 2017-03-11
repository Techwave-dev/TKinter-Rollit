#!/usr/bin/python
#-*-coding: utf-8 -*-

from Tkinter import *
import Tkinter
import tkMessageBox
import random
import tkFont

#TODO redimensionnement fenetre

class NbEntry(Tk):
        def __init__(self):
                Tk.__init__(self)

                self.title("Configuration")
                self.label = Label(self, text="Entrer le nombre de cases sur le coté")
                self.label.pack()

                self.entry = Entry(self)
                self.entry.pack()
                
                self.valider = Button(self, text="Valider", command=self.valider)
                self.valider.pack()
                
        def valider(self):
                nbCases = int(self.entry.get())
                try:
                        if nbCases < 8 or nbCases % 2 != 0:
                                tkMessageBox.showerror("Erreur", "Le nombre doit être supérieur ou égal à 8 et doit être pair!")
                                return
                except ValueError:
                        tkMessageBox.showerror("Erreur", "Vous devez rentrer un nombre!")
                        return

                self.destroy()
                window = MainWindow(nbCases)
                window.mainloop()

                
class MainWindow(Tk):
        
        def __init__(self, nbCases):
                Tk.__init__(self)
                
                self.nbCase = nbCases
                
                self.init()     
                self.font = tkFont.Font(family="Times", size=32, weight="bold", underline=1)
                self.fontScores = tkFont.Font(family="Times", size=16)
                self.tileSize = 480.0 / len(self.gameState)               
                self.lastX = -2*self.tileSize
                self.lastY = -2*self.tileSize

                self.configure(width=480, height=480)
                self.title("Rollit")
                self.canvas = Canvas(width=480, height=480)
                self.canvas.pack()              
                
                
                self.canvas.bind("<Motion>", self.motion)
                self.canvas.bind("<Button-1>", self.ajouterPiont)
                self.bind("<Return>", self.restart)
                self.bind("<F1>", self.fillAll)
                #self.bind("<Configure>", self.resize)

                self.update()
                
        def resize(self, event):
                minValue = min(event.width, event.height)
                self.tileSize = float(minValue) / len(self.gameState)
                self.canvas.configure(width=minValue, height=minValue)
                
        def fillAll(self, event):
                for i in range(len(self.gameState)):
                                for j in range(len(self.gameState[i])):
                                        self.gameState[i] = setChar(self.gameState[i], j, str(random.randrange(2)+1))

        def restart(self, event):
                if self.aGagner:
                        self.init()

        def init(self):
                self.aGagner = False
                self.joueurEnCours = 1

                self.gameState = []
                for x in range(self.nbCase):
                        self.gameState.append("0"*self.nbCase)
                
                self.gameState[len(self.gameState)/2] = setChar(self.gameState[len(self.gameState)/2], len(self.gameState)/2, "1")
                self.gameState[len(self.gameState)/2-1] = setChar(self.gameState[len(self.gameState)/2-1], len(self.gameState)/2, "2")
                self.gameState[len(self.gameState)/2] = setChar(self.gameState[len(self.gameState)/2], len(self.gameState)/2-1, "2")
                self.gameState[len(self.gameState)/2-1] = setChar(self.gameState[len(self.gameState)/2-1], len(self.gameState)/2-1, "1")


        def update(self):
                if self.gagnant():
                        self.aGagner = True             
                        
                self.render()

                self.after(1000/60, self.update)

        def render(self):
                #self.canvas.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), fill="#FFFFFF") <- A ne pas faire, on ne vide pas l'ecran on masque juste les anciens elements
                self.canvas.delete(ALL)         

                for i in range(0, len(self.gameState)+1):
                        self.canvas.create_line(0, i*self.tileSize, self.canvas.winfo_width(), i*self.tileSize, fill="#999999")
                for j in range(0, len(self.gameState)+1):
                        self.canvas.create_line(j * self.tileSize, 0, j * self.tileSize, self.canvas.winfo_height(), fill="#999999")
                
                for i in range(len(self.gameState)):    
                        for j in range(len(self.gameState[i])):
                                if self.gameState[i][j] == "1" :
                                        self.canvas.create_rectangle(j * self.tileSize, i * self.tileSize, j * self.tileSize + self.tileSize, i * self.tileSize + self.tileSize, fill="#FF00FF")                
                                if self.gameState[i][j] == "2" :
                                        self.canvas.create_rectangle(j * self.tileSize, i * self.tileSize, j * self.tileSize + self.tileSize, i * self.tileSize + self.tileSize, fill="#00FF00")
                                
                if self.joueurEnCours == 1:
                        self.canvas.create_rectangle(self.lastX - self.tileSize/2/2, self.lastY - self.tileSize/2/2, self.lastX + self.tileSize/2/2, self.lastY + self.tileSize/2/2, fill="#FF00FF")
                else:
                        self.canvas.create_rectangle(self.lastX - self.tileSize/2/2, self.lastY - self.tileSize/2/2, self.lastX + self.tileSize/2/2, self.lastY + self.tileSize/2/2, fill="#00FF00")
                if self.aGagner:
                        joueur1Points = 0
                        joueur2Points = 0
                        for i in range(len(self.gameState)):
                                for j in range(len(self.gameState[i])):
                                        if self.gameState[i][j] == "1":
                                                joueur1Points = joueur1Points + 1
                                        else:
                                                joueur2Points = joueur2Points + 1
                                                
                        if joueur1Points > joueur2Points:
                                self.canvas.create_text(self.winfo_width()/2, (self.winfo_height()/4)*1.5, text="Le joueur 1 à gagné!", font=self.font)
                        elif joueur1Points < joueur2Points:
                                self.canvas.create_text(self.winfo_width()/2, (self.winfo_height()/4)*1.5, text="Le joueur 2 à gagné!", font=self.font)
                        else:
                                self.canvas.create_text(self.winfo_width()/2, (self.winfo_height()/4)*1.5, text="Égalité!", font=self.font)
                                
                        self.canvas.create_text(self.winfo_width()/2, (self.winfo_height()/4)*1.5+32+20, text="Joueur 1: " + str(joueur1Points), font=self.fontScores)
                        self.canvas.create_text(self.winfo_width()/2, (self.winfo_height()/4)*1.5+16+32+20+5, text="Joueur 2: " + str(joueur2Points), font=self.fontScores)
                        
                
        def gagnant(self):
                for i in range(len(self.gameState)):
                        for j in range(len(self.gameState)):
                                if self.gameState[i][j] == "0":
                                        return False
                return True
        
        def ajouterPiont(self, event):
                if self.aGagner:
                        return          

                y = event.y / self.tileSize
                x = event.x / self.tileSize

                y = int(y)
                x = int(x)

                if self.gameState[y][x] != "0":
                        return

                if self.joueurEnCours == 1:
                        self.gameState[y] = setChar(self.gameState[y], x, "1")
                else:
                        self.gameState[y] =  setChar(self.gameState[y], x, "2")

                #gauche
                nb = 2
                for xDir in range(x-1,-1,-1):
                        if self.gameState[y][xDir] == "0":
                                break
                        if self.gameState[y][xDir] == str(self.joueurEnCours):
                                for i in range(nb):
                                        self.gameState[y] = setChar(self.gameState[y], x-i, str(self.joueurEnCours))
                                break
                        else:
                                nb = nb +1
                                
                #droite
                nb = 2
                for xDir in range(x+1, len(self.gameState[y])):
                        if self.gameState[y][xDir] == "0":
                                break
                        if self.gameState[y][xDir] == str(self.joueurEnCours):
                                for i in range(nb):
                                        self.gameState[y] = setChar(self.gameState[y], x+i, str(self.joueurEnCours))
                                break
                        else:
                                nb = nb +1
                                
                #bas
                nb = 2
                for yDir in range(y+1,len(self.gameState)):
                        if self.gameState[yDir][x] == "0":
                                break
                        if self.gameState[yDir][x] == str(self.joueurEnCours):
                                for i in range(nb):
                                        self.gameState[y+i] = setChar(self.gameState[y+i], x, str(self.joueurEnCours))
                                break
                        else:
                                nb = nb +1
                                
                #haut
                nb = 2
                for yDir in range(y-1,-1, -1):
                        if self.gameState[yDir][x] == "0":
                                break
                        if self.gameState[yDir][x] == str(self.joueurEnCours):
                                for i in range(nb):
                                        self.gameState[y-i] = setChar(self.gameState[y-i], x, str(self.joueurEnCours))
                                break
                        else:
                                nb = nb +1
                                
                #bas-droite
                nb = 2
                for dirXY in range(1, min(len(self.gameState)-y, (len(self.gameState[y])-x))):
                        if self.gameState[y+dirXY][x+dirXY] == "0":
                                break
                        if self.gameState[y+dirXY][x+dirXY] == str(self.joueurEnCours):
                                for i in range(nb):
                                        self.gameState[y+i] = setChar(self.gameState[y+i], x+i, str(self.joueurEnCours))
                                break
                        else:
                                nb = nb +1
                                
                #bas-gauche
                nb = 2
                for dirXY in range(1, min(len(self.gameState)-y, x+1)):
                        if self.gameState[y+dirXY][x-dirXY] == "0":
                                break
                        if self.gameState[y+dirXY][x-dirXY] == str(self.joueurEnCours):
                                for i in range(nb):
                                        self.gameState[y+i] = setChar(self.gameState[y+i], x-i, str(self.joueurEnCours))
                                break
                        else:
                                nb = nb +1
                                
                #haut-gauche
                nb = 2
                for dirXY in range(1, min(y+1, x+1)):
                        if self.gameState[y-dirXY][x-dirXY] == "0":
                                break
                        if self.gameState[y-dirXY][x-dirXY] == str(self.joueurEnCours):
                                for i in range(nb):
                                        self.gameState[y-i] = setChar(self.gameState[y-i], x-i, str(self.joueurEnCours))
                                break
                        else:
                                nb = nb +1
                                
                #haut-droite
                nb = 2
                for dirXY in range(1, min(y+1, (len(self.gameState[y])-x))):
                        if self.gameState[y-dirXY][x+dirXY] == "0":
                                break
                        if self.gameState[y-dirXY][x+dirXY] == str(self.joueurEnCours):
                                for i in range(nb):
                                        self.gameState[y-i] = setChar(self.gameState[y-i], x+i, str(self.joueurEnCours))
                                break
                        else:
                                nb = nb +1

                self.joueurEnCours = self.joueurEnCours + 1
                if self.joueurEnCours > 2:
                        self.joueurEnCours = 1
                        
        def motion(self, event):
                self.lastX = event.x
                self.lastY = event.y
                
def setChar(string, index, char):
        string = string[:index] + char + string[index+1:]
        return string
                
if __name__ == "__main__":
        window = NbEntry()
        window.mainloop()
