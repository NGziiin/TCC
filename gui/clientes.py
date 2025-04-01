from tkinter import *
import sys
import os
from functools import partial

#todos os imports de arquivos ficam aqui
def imports():

    ## janela dos botões adicionados
    gui_for_button = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(gui_for_button, 'button_gui'))
    global window_register
    from gui.button_gui.gui_add_clients import window_register


def lista_clientes(frameinfo):
    imports()

    frameclients = LabelFrame(frameinfo, bg='white', border=0)
    frameclients.place(relheight=0.9, relwidth=0.99, rely=0.25, relx=0.005)
    
def janela_clientes(frameinfo):

    imports()
    
    framelist = LabelFrame(frameinfo, bg='green', border=0)
    framelist.place(relheight=0.05, relwidth=1, rely=0.2)

    register_button = Button(frameinfo, text='REGISTRAR', font=('arial', 20, 'bold'), bg='white', fg='black', border=0, command=partial(window_register))
    register_button.place(y=144, x=530)

    view_client_button = Button(frameinfo, text='VISUALIZAR', font=('arial', 20, 'bold'), bg='white', fg='black', border=0)
    view_client_button.place(y=144, x=730)

    client_history = Button(frameinfo, text='HISTÓRICO', font=('arial', 20, 'bold'), bg='white', fg='black', border=0)
    client_history.place(y=144, x=930)

    search_clients = Entry(framelist, font=('arial', 20), bg='white', fg='black')
    search_clients.place(y=10, x=10, width=800, height=30)

    btn_client_search = Button(framelist, text='BUSCAR', font=('arial', 16), bg='white', fg='black', border=0)
    btn_client_search.place(y=10, x=820, width=150, height=30)