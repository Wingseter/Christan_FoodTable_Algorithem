from tkinter import *

def data():
    for i in range(50):
       Label(t_frame,text=i).grid(row=i,column=0)
       Label(t_frame,text="my text"+str(i)).grid(row=i,column=1)
       Label(t_frame,text="..........").grid(row=i,column=2)

def scroll_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)

root=Tk()
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

table_frame=Frame(root,relief=GROOVE, bd=1, padx = 1, pady = 1)
table_frame.pack(side="right", fill="x", expand=True, padx = 5, pady = 5)

canvas=Canvas(table_frame)
t_frame=Frame(canvas)
table_scroll=Scrollbar(table_frame,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=table_scroll.set)

table_scroll.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=t_frame,anchor='nw')
t_frame.bind("<Configure>",scroll_configure)
data()
root.mainloop()