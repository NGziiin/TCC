from tkinter import *

def botoes():
    btn1 = Button(framebutton, text='Vendas', font=('arial', 16))
    btn1.place(relheight=0.05, relwidth=1, relx=0, rely=0.3)
    btn2 = Button(framebutton, text='Estoque', font=('arial', 16))
    btn2.place(relheight=0.05, relwidth=1, relx=0, rely=0.36)

janela = Tk()

janela.geometry('1920x1040')
janela.state('zoomed')
janela.configure(bg='blue')

framebutton = Frame(janela, bg='white')
framebutton.place(relheight=0.99, relwidth=0.15, relx=0.002, rely=0.005)

frameinfo = Frame(janela, bg='green')
frameinfo.place(relheight=0.99, relwidth=0.842, relx=0.155, rely=0.005)

botoes()

janela.mainloop()