from tkinter import *
index={'Food':['apple', 'orange'], 'Drink':['juice', 'water', 'soda']}
Names=['Food', 'Drink']

def display(item):
    print(item)

mon=Tk()
app=Frame(mon)
app.grid()

for item in range(25):
    Button(mon, text=item, command= lambda name = item: display(name)).grid()
mon.mainloop()