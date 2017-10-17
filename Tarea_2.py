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
        s = simpledialog.askstring("¡Bienvenido al juego del coyote y las gallinas!","¿Quieres cargar una partida (1) o empezar de nuevo (2)?")
        while s!="1" and s!="2":
            s = simpledialog.askstring("Input Invalido", "Por favor ingrese una instrucción valida")
        
        if s=="1":
            s = askopenfilename()
            while s=="":
                s = askopenfilename()
            self.load(file)
        else:
            self.tablero = 25*[25*[0]]
            self.marcado = 25*[-1]
            self.turno = 0
            self.players = []
            self.players.append(simpledialog.askstring("Coyote","Ingrese el nombre del jugador que será el Coyote"))
            self.players.append(simpledialog.askstring("Gallinas","Ingrese el nombre del jugador que será las Gallinas"))
            self.temp = -1
            for i in range(25):
                if i < 11:
                    self.marcado[i]=0
                if i == 12:
                    self.marcado[i]=1
                if i == 14:
                    self.marcado[i]=0
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
                    if i>1 and self.tablero[i][i-1]=1:
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
                    if i>9 and self.tablero[i][i-5]=1:
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
                            self.tablero[i][i-8]==2
                            self.tablero[i-8][i]==2
                    if not (l or u):
                        self.tablero[i][i-6]=1
                        self.tablero[i-6][i]=1
                    if not (l or d):
                        self.tablero[i][i+4]=1
                        self.tablero[i+4][i]=1
                        if i>9 and self.tablero[i][i-6]==1:
                            self.tablero[i][i-12]==2
                            self.tablero[i-12][i]==2
                        
    def move1(self, pos):
        if self.temp==-1:
            self.temp = pos
        elif pos == self.temp:
            self.temp=-1
        else:
            a = self.move2(self.temp, pos)
            if a[0] and not a[1]:
                messagebox.showinfo("Info","Es tu turno "+self.players[self.turno%2])
                self.temp = pos
            elif a[0]:
                self.temp = -1
            else:
                messagebox.showinfo("Error",a[1])


    def move2(self, m1, m2):
        if self.marcado[m1]!=self.turno%2:
            return [False, "Por favor elegir ficha valida"]
        if not (self.tablero[m1][m2]==1 or (self.tablero[m1][m2]==2 and self.marcado[(m1+m2)/2]=0)) or (self.marcado[m2]!=-1):
            return [False, "Por favor ingrese movimiento valido"]
        self.marcado[m1] = -1
        self.marcado[m2] = self.turno%2
        if self.turno%2==1 and self.tablero[m1][m2]==2:
            return [True, True]
        self.turno = self.turno + 1
        return [True, False]

    def win(self):
        if self.marcado.count(-1)<11:
            return [True, 1, "Gano el coyote"]
        a = self.marcado.index(1)
        for i in len(self.tablero[a]):
            if (self.tablero[a][i]==1 or self.tablero[a][i]==2) and not self.marcado[i]==0:
                return [False]
        return [True, 0]

    def load(self, file):
        with open(file, 'r') as f:
            data = f.readlines()
    
    def save(self):
        print("Ingrese nombre para el archivo:")
        s = input()
        while s is not str:
            print("Ingrese nombre valido para el archivo:")
            s = input()

    def build_GUI(self):
        self.loadgame = tk.Button(self, text="Cargar Partida")
        self.loadgame.pack(side="bottom")
        self.loadgame.config(command=self.load)
        self.savegame = tk.Button(self, text="Guardar Partida")
        self.savegame.pack(side="bottom")
        self.savegame.config(command=self.save)
        group_master = tk.LabelFrame(self, text="Tablero", padx=10, pady=10)
        for i in range(5):
            group = tk.Frame(group_master)
            for j in range(5):
                button = tk.Button(group, text=0, command= lambda place=5*i+j: move1(place))
                button.grid(row = 2*i, column=2*j)
                if j!=4:
                    label = tk.Label(group, text="-")
                    label.grid(row = 2*i, column = 2*j+1)
            group.pack(padx=10, pady=10, side="right")
            group = tk.Frame(group_master)
            for j in range(5):
                label1 = tk.Label(group, text="|")
                label1.grid(row = 2*i+1, column = 2*j)
                if j!=4:
                    if j%2==0:
                        label2 = tk.Label(group, text="\")
                    else:
                        label2 = tk.Label(group, text="/")
                    label2.grid(row = 2*i, column = 2*j+1)
            group.pack(padx=10,pady=10, side="right")
        


g = Game()
g.mainloop()


