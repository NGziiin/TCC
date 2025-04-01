from tkinter import *

def add_list(frameclients):
    print('botão foi chamado na função add_list')

    teste = Label(frameclients, text='teste', font=('arial', 16), bg='white', fg='black')
    teste.pack(padx = 1, pady = 1)

    if teste is not None:
        print(f"adicionou a informação {teste}")