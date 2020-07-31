from tkinter import *
import winsound
from winsound import *
from tkinter import messagebox
import time

#creamos la ventana

raiz=Tk()

raiz.title("MYRIAD ALLIANCE: ORIGINS")
raiz.geometry("900x550")
# raiz.resizable(0,0)
# raiz.iconbitmap("C:\\Users\\shado\\Desktop\\Myadorigins\\descarga.ico")

frameJugar = Frame()

fondo = PhotoImage(file="background.png")
background_label = Label(raiz, image=fondo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


raiz.mainloop()