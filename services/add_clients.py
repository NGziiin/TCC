from tkinter import *

def add_list(frameclients):

    print('botão foi chamado na função add_list')
    if frameclients is not None:
        print(f'frameclients está com o parâmetro {frameclients}')
    teste = Label(frameclients, text='teste')
    teste.pack(padx=10, pady=10)
