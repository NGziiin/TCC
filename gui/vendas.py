from tkinter import *

def janela_vendas(frameinfo):

    button = Button(frameinfo, text='CONFIRMAR', font=('arial', 20, 'bold'), bg='green', fg='white', border=0)
    button.place(y=800, x=1100)

    label_codigo = LabelFrame(frameinfo, bg='green', border=0)
    label_codigo.place(y=0, x=0, relheight=0.06, relwidth=0.2)

    text_codigo = Label(label_codigo, text='CÓDIGO DO PRODUTO')
    text_codigo.pack(anchor='sw', pady=5)
    entry_codigo = Entry(label_codigo)
    entry_codigo.pack(expand=True, fill=X)