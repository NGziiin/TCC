from tkinter import *

def janela_vendas(frameinfo):
    print('chegou na janela de vendas')

    button = Button(frameinfo, text='CONFIRMAR', font=('arial', 35, 'bold'), bg='green', fg='white', border=0)
    button.pack(anchor='se')