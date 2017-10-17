# -*- coding: utf-8 -*-
import math
import os.path
import tkinter.simpledialog as tk
from tkinter.filedialog import askopenfilename
 
class Game:

    def __init__(self, file, players):
        if file is not None:
            self.load(file)
            return
        self.tablero = []
        self.marcado = 25*[-1]
        self.turno = 0
        self.players = players
        for i in range(25):
            if i < 11:
                self.marcado[i]=0
            if i == 12:
                self.marcado[i]=1
            if i == 14:
                self.marcado[i]=0
        for i in range(25):
            self.tablero.append([])
            r = True
            l = True
            u = True
            d = True
            if i%5!=4:
                self.tablero[i].append(i+1)
                r = False
            if i%5!=0:
                self.tablero[i].append(i-1)
                l = False
            if math.floor(i/5)!=4:
                self.tablero[i].append(i+5)
                d = False
            if math.floor(i/5)!=0:
                self.tablero[i].append(i-5)
                u = False
            if i%2==0:
                if not (r or u):
                    self.tablero[i].append(i-4)
                if not (r or d):
                    self.tablero[i].append(i+6)
                if not (l or u):
                    self.tablero[i].append(i-6)
                if not (l or d):
                    self.tablero[i].append(i+4)
    
    def move(self, x1, y1, x2, y2):
        if x1<0 or x1>4 or y1<0 or y1>4 or x2<0 or x2>4 or y2<0 or y2>4:
            return [False, "Por favor ingrese coordenadas validas"]
        if self.marcado[x1+5*y1]!=self.turno%2:
            return [False, "Por favor elegir ficha valida"]
        if x1==x2 and y1==y2:
            return [False, "Por favor mover a una posición distinta a la original"]
        if not (x2+5*y2 in self.tablero[x1+5*y1]) or (self.marcado[x2+5*y2]!=-1):
            return [False, "Por favor ingrese movimiento valido"]
        self.marcado[x1+5*y1] = -1
        self.marcado[x2+5*y2] = self.turno%2
        if self.turno%2==1:
            return [True, True]
        self.turno = self.turno + 1
        return [True, False]

    def win(self):
        if self.marcado.count(-1)<11:
            return [True, 1]
        a = self.marcado.index(1)
        for i in self.tablero[a]:
            if self.marcado[i]==-1:
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

print("¡Bienvenido al juego del coyote y las gallinas!")
print("¿Quieres cargar una partida (1) o empezar de nuevo (2)?")
s = input()
while s!="1" and s!="2":
    print("Por favor ingrese una instrucción valida")
    s = input()
if s=="1":
    s = askopenfilename()
    while s=="":
        s = askopenfilename()
    gm = Game(s)
else:
    names = []
    names.append(tk.askstring("Coyote","Ingrese el nombre del jugador que será el Coyote"))
    names.append(tk.askstring("Gallinas","Ingrese el nombre del jugador que será las Gallinas"))
    gm = Game(None, names)

while(not gm.win()[0]):
    pass


