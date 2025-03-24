from tkinter import *

def janela_clientes(frameinfo):
    
    framelist = LabelFrame(frameinfo, bg='green', border=0)
    framelist.place(relheight=0.8, relwidth=1, rely=0.2)

    register_button = Button(frameinfo, text='REGISTRAR', font=('arial', 20, 'bold'), bg='white', fg='black', border=0)
    register_button.place(y=800, x=1100)