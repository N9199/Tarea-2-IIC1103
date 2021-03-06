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
        messagebox.showinfo("Juego del coyote y de las gallinas","Bienvenidos, jugadores!")
        self.pack()
        self.build_GUI()
        self.start()
        self.new()
        
        messagebox.showinfo("Info","Cada movimiento consiste en seleccionar una ficha y despues seleccionar la posición a la cual mover la ficha. Comienzan las gallinas.")
        self.update()
        #for i in range(25):
            #print(self.tablero[i])
        #for i in range(25):
            #for j in range(25):
                #if self.tablero[i][j]!=self.tablero[j][i]:
                    #print(i,j,self.tablero[i][j],self.tablero[j][i])

    def savestatus(self, m1, m2):
        t = {}
        t[0]="G"
        t[1]="C"
        self.history.append(t[self.turno%2]+","+str(m1%5)+","+str(int(math.floor(m1/5)))+","+str(m2%5)+","+str(int(math.floor(m2/5))))
        print(self.history[-1])
        print(self)

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
                    if j!=4:
                        if j%2==i%2:
                            d+="\\"
                        else:
                            d+="/"
                s+=d+"\n"
        return s

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
        if messagebox.askyesno("Info","¿Quieren cargar una partida?"):
            self.load()
        else:
            self.players[0]=simpledialog.askstring("Gallinas","Ingrese el nombre del jugador que será las Gallinas.")
            self.players[1]=simpledialog.askstring("Coyote","Ingrese el nombre del jugador que será el Coyote.")
    
    def start(self):
        self.players = ["",""]
        self.tablero = []
        self.history = []
        for i in range(25):
            temp = []
            for j in range(25):
                temp.append(0)
            self.tablero.append(temp)
        self.marcado = 25*[-1]
        self.turno = 0
        self.temp = -1
        self.temp0 = True
        for i in range(25):
            #print(i)
            r = True
            l = True
            u = True
            d = True
            if i%5!=4:
                self.tablero[i][i+1]=1
                self.tablero[i+1][i]=1
                #print(self.tablero[i+1][i],i,i+1)
                #if i==20 or i==19:
                    #print("WTF?")
                r = False
            if i%5!=0:
                self.tablero[i][i-1]=1
                self.tablero[i-1][i]=1
                #print(self.tablero[i-1][i],i,i-1)
                #if i==21 or i==20:
                    #print("WTF?")
                l = False
                if i>1 and self.tablero[i][i-1]==1 and i%5>1:
                    self.tablero[i][i-2]=2
                    self.tablero[i-2][i]=2
                    #print(self.tablero[i][i-1],self.tablero[i-2][i],i,i-2)
            if math.floor(i/5)!=4:
                self.tablero[i][i+5]=1
                self.tablero[i+5][i]=1
                #print(self.tablero[i+5][i])
                d = False
            if math.floor(i/5)!=0:
                self.tablero[i][i-5]=1
                self.tablero[i-5][i]=1
                #print(self.tablero[i-5][i])
                u = False
                if i>9 and self.tablero[i][i-5]==1 and math.floor(i/5)>1:
                    self.tablero[i][i-10]=2
                    self.tablero[i-10][i]=2
                    #print(self.tablero[i-10][i])
            if i%2==0:
                if not (r or u):
                    self.tablero[i][i-4]=1
                    self.tablero[i-4][i]=1
                    #print(self.tablero[i-4][i])
                    if i>9 and self.tablero[i][i-4]==1:
                        #print(i,i-8)
                        self.tablero[i][i-8]=2
                        self.tablero[i-8][i]=2
                        #print(self.tablero[i-8][i])
                if not (r or d):
                    self.tablero[i][i+6]=1
                    self.tablero[i+6][i]=1
                    #print(self.tablero[i+6][i])
                if not (l or u):
                    self.tablero[i][i-6]=1
                    self.tablero[i-6][i]=1
                    #print(self.tablero[i-6][i])
                    if i>9 and self.tablero[i][i-6]==1:
                        #print(i,i-12)
                        self.tablero[i][i-12]=2
                        self.tablero[i-12][i]=2
                        #print(self.tablero[i-12][i])
                if not (l or d):
                    self.tablero[i][i+4]=1
                    self.tablero[i+4][i]=1
                    #print(self.tablero[i+4][i])

    def move1(self, pos):
        #print(pos,self.marcado[pos],self.turno%2)
        if self.temp==-1:
            if self.marcado[pos]!=self.turno%2:
                messagebox.showinfo("Error","Por favor seleccionar ficha valida.")
                return
            self.temp = pos
            self.buttons[pos].config(background='blue')
        elif pos == self.temp:
            self.temp=-1
            self.buttons[pos].config(background='SystemButtonFace')
        else:
            a = self.move2(self.temp, pos)
            b = self.win()
            #print(b)
            if b[0]:
                self.buttons[self.temp].config(background='SystemButtonFace')
                messagebox.showinfo("Felicitaciones", self.players[b[1]]+" has ganado.")
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
                self.buttons[self.temp].config(background='SystemButtonFace')
            elif a[0]:
                self.buttons[self.temp].config(background='SystemButtonFace')
                messagebox.showinfo("Info","Es tu turno "+self.players[self.turno%2]+" ¿Cual sera tu movimiento? Si quieres cargar o guardar, apreta los botones corespondientes.")
                self.update()
                self.temp = -1
            else:
                messagebox.showinfo("Error",a[1])


    def move2(self, m1, m2):
        if not (self.tablero[m1][m2]==1 or (self.tablero[m1][m2]==2 and self.marcado[int((m1+m2)/2)]==0)) or (self.marcado[m2]!=-1):
            #print(self.tablero[m1][m2],self.marcado[int((m1+m2)/2)],self.marcado[m2])
            return [False, "Por favor ingrese movimiento valido."]
        temp = True
        for i in range(25):
            if self.turno%2==1 and self.tablero[m1][i]==2 and self.marcado[int((m1+i)/2)]==0 and self.marcado[i]==-1:
                if i==m2 or self.temp0:
                    temp = True
                    break
                else:
                    temp = False
        if not temp:
            return [False, "El coyote tiene que comer si es que puede."]
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
                if self.tablero[m2][i]==2 and self.marcado[int((m2+i)/2)]==0 and self.marcado[i]==-1:
                    self.savestatus(m1,m2)
                    self.temp0 = False
                    return [True, True]
        self.savestatus(m1,m2)
        self.turno = self.turno + 1
        self.temp0 = True 
        return [True, False]

    def win(self):
        if not self.temp0:
            return [False, "temp0"]
        if self.marcado.count(0)<11:
            return [True, 1]
        a = self.marcado.index(1)
        #print(len(self.tablero[a]))
        for i in range(len(self.tablero[a])):
            #print("win:",a,i,self.tablero[a][i],self.marcado[i])
            if (self.tablero[a][i]==1 or self.tablero[a][i]==2) and self.marcado[i]==-1:
                return [False]
        return [True, 0]

    def load(self):
        file = askopenfilename()
        if file =="":
            return
        with open(file, 'r') as f:
            data = f.readlines()
        self.players=data[0][:-1].split(",")
        print(self)
        for i in range(1,len(data)):
            a = data[i][:-1].split(",")
            self.move2(int(a[1])+5*int(a[2]),int(a[3])+5*int(a[4]))
    
    def save(self):
        s = simpledialog.askstring("Info","Ingrese nombre para el archivo:")
        if len(s)>4:
            if s[-4]!=".txt":
                s+=".txt"
        else:
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


