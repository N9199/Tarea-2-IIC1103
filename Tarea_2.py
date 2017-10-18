# -*- coding: utf-8 -*-
import math
import os.path
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


class Game(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.build_GUI()
        self.start()
        if messagebox.askyesno("Info","¿Quieren cargar una partida?"):
            self.load()
        else:
            self.new()
            self.players.append(simpledialog.askstring("Gallinas","Ingrese el nombre del jugador que será las Gallinas"))
            self.players.append(simpledialog.askstring("Coyote","Ingrese el nombre del jugador que será el Coyote"))
        messagebox.showinfo("Info","Cada movimiento consiste en seleccionar una ficha y despues seleccionar una posición a la cual mover la ficha. Comienzan las gallinas")
        self.update()

    def savestatus(self, m1, m2):
        t = {}
        t[0]="G"
        t[1]="C"
        self.history.append(t[self.turno%2]+","+str(m1%5)+","+str(int(math.floor(m1/5)))+","+str(m2%5)+","+str(int(math.floor(m2/5))))
        print(self.history[-1])

    def __str__(self):
        t = {}
        t[-1]="N"
        t[0]="G"
        t[1]="C"
        s = ""
        for i in range(5):
            d = ""
            for j in range(5):
                d+=t[self.marcado[5*i+j]]
                if j!=4:
                    d+="-"
            s+=d+"\n"
            if i!=4:
                d = ""
                for j in range(5):
                    d+="|"
                    if j%2==i%2:
                        d+="\\"
                    else:
                        d+="/"
                s+=d+"\n"

    def new(self):
        for i in range(25):
            if i < 11:
                self.marcado[i]=0
            elif i == 12:
                self.marcado[i]=1
            elif i == 14:
                self.marcado[i]=0
            else:
                self.marcado[i]=-1
        self.turno = 0
        self.temp = -1
        t = {}
        t[-1]="N"
        t[0]="G"
        t[1]="C"
        for i in range(25):
            self.buttons[i].config(text=t[self.marcado[i]])
        self.history = []
    
    def start(self):
        self.players = []
        self.tablero = []
        for i in range(25):
            temp = []
            for j in range(25):
                temp.append(0)
            self.tablero.append(temp)
        self.marcado = 25*[-1]
        self.turno = 0
        self.temp = -1
        for i in range(25):
            r = True
            l = True
            u = True
            d = True
            if i%5!=4:
                self.tablero[i][i+1]=1
                self.tablero[i+1][i]=1
                r = False
            if i%5!=0:
                self.tablero[i][i-1]=1
                self.tablero[i-1][i]=1
                l = False
                if i>1 and self.tablero[i][i-1]==1:
                    self.tablero[i][i-2]=2
                    self.tablero[i-2][i]=2
            if math.floor(i/5)!=4:
                self.tablero[i][i+5]=1
                self.tablero[i+1][i]=1
                d = False
            if math.floor(i/5)!=0:
                self.tablero[i][i-5]=1
                self.tablero[i-5][i]=1
                u = False
                if i>9 and self.tablero[i][i-5]==1:
                    self.tablero[i][i-10]=2
                    self.tablero[i-10][i]=2
            if i%2==0:
                if not (r or u):
                    self.tablero[i][i-4]=1
                    self.tablero[i-4][i]=1
                if not (r or d):
                    self.tablero[i][i+6]=1
                    self.tablero[i+6][i]=1
                    if i>9 and self.tablero[i][i-4]==1:
                        #print(i,i-8)
                        self.tablero[i][i-8]==2
                        self.tablero[i-8][i]==2
                if not (l or u):
                    self.tablero[i][i-6]=1
                    self.tablero[i-6][i]=1
                if not (l or d):
                    self.tablero[i][i+4]=1
                    self.tablero[i+4][i]=1
                    if i>9 and self.tablero[i][i-6]==1:
                        #print(i,i-12)
                        self.tablero[i][i-12]==2
                        self.tablero[i-12][i]==2

    def move1(self, pos):
        #print(pos,self.marcado[pos],self.turno%2)
        if self.temp==-1:
            if self.marcado[pos]!=self.turno%2:
                messagebox.showinfo("Error","Por favor seleccionar ficha valida")
                return
            self.temp = pos
            self.buttons[pos].config(background='blue')
        elif pos == self.temp:
            self.temp=-1
            self.buttons[pos].config(background='white')
        else:
            a = self.move2(self.temp, pos)
            b = self.win()
            if b[0]:
                messagebox.showinfo("Felicitaciones", self.players[b[1]]+" has ganado")
                if messagebox.askyesno("Info","Quieren guardar el juego?"):
                    self.save()
                if messagebox.askyesno("Info","Quieren jugar un juego nuevo?"):
                    self.new()
                    return
                else:
                    self.quit()
                    return
            if a[0] and a[1]:
                self.temp = pos
            elif a[0]:
                messagebox.showinfo("Info","Es tu turno "+self.players[self.turno%2])
                self.update()
                self.temp = -1
            else:
                messagebox.showinfo("Error",a[1])


    def move2(self, m1, m2):
        if not (self.tablero[m1][m2]==1 or (self.tablero[m1][m2]==2 and self.marcado[int((m1+m2)/2)]==0)) or (self.marcado[m2]!=-1):
            #print(self.tablero[m1][m2],self.marcado[int((m1+m2)/2)],self.marcado[m2])
            return [False, "Por favor ingrese movimiento valido"]
        t = {}
        t[-1]="N"
        t[0]="G"
        t[1]="C"
        self.marcado[m1] = -1
        self.marcado[m2] = self.turno%2
        self.buttons[m1].config(text="N")
        self.buttons[m2].config(text=t[self.turno%2])
        if self.turno%2==1 and self.tablero[m1][m2]==2:
            self.marcado[int((m1+m2)/2)]=-1
            self.buttons[int((m1+m2)/2)].config(text="N")
            for i in range(25):
                if self.tablero[m2][i]==2 and self.marcado[int((m1+m2)/2)]==0 and self.marcado[i]==-1:
                    #print(self.tablero[m2][i],self.marcado[int((m1+m2)/2)],self.marcado[i])
                    self.savestatus(m1,m2)
                    return [True, True]
        self.savestatus(m1,m2)
        self.turno = self.turno + 1
        return [True, False]

    def win(self):
        if self.marcado.count(0)<11:
            return [True, 1]
        a = self.marcado.index(1)
        for i in range(len(self.tablero[a])):
            if (self.tablero[a][i]==1 or self.tablero[a][i]==2) and not self.marcado[i]==-1:
                return [False]
        return [True, 0]

    def load(self):
        file = askopenfilename()
        while file=="":
            file = askopenfilename()
        with open(file, 'r') as f:
            data = f.readlines()
        self.players=data[0][:-2].split(",")
        for i in range(1,len(data)):
            self.history.append(data[i][:-2])
            
    
    def save(self):
        s = simpledialog.askstring("Info","Ingrese nombre para el archivo:")
        if s[-4]!=".txt":
            s+=".txt"
        with open(s, 'w') as f:
            f.write(self.players[0]+","+self.players[1]+"\n")
            for line in self.history:
                f.write(line+"\n")        

    def build_GUI(self):
        self.loadgame = tk.Button(self, text="Cargar Partida")
        self.loadgame.pack(side="bottom")
        self.loadgame.config(command=self.load)
        self.savegame = tk.Button(self, text="Guardar Partida")
        self.savegame.pack(side="bottom")
        self.savegame.config(command=self.save)
        self.buttons = []
        group_master = tk.LabelFrame(self, text="Tablero", padx=10, pady=10)
        for i in range(5):
            group = tk.Frame(group_master)
            for j in range(5):
                button = tk.Button(group, text=0, command= lambda place=(5*i+j): self.move1(place))
                self.buttons.append(button)
                button.grid(row = 2*i, column=2*j)
                if j!=4:
                    label = tk.Label(group, text="-")
                    label.grid(row = 2*i, column = 2*j+1)
            group.pack(padx=10, side="top")
            group = tk.Frame(group_master)
            if i!=4:
                templabel = ""
                for j in range(5):
                    templabel += "|"
                    if j!=4:
                        templabel+="     "
                        if j%2==i%2:
                            templabel+="\\"
                        else:
                            templabel+="/"
                        templabel+="     "
                label = tk.Label(group, text=templabel)
                label.grid(row = 2*i+1, column = 0)
                group.pack(padx=10, side="top")
        group_master.pack(pady=20, padx=10)

G = Game()
G.mainloop()


