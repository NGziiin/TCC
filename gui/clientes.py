from tkinter import *
import sys
import os
from functools import partial

#todos os imports de arquivos ficam aqui
def imports():

    ## janela dos botões adicionados
    gui_for_button = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(gui_for_button, 'button_clients'))
    global window_register
    global StartUI
    from button_clients.gui_add_clients import window_register
    from button_clients.gui_view_clients import StartUI

def frame_lista_clientes(frameclients):
    global frame_nome
    global frame_cpf
    global frame_cidade
    global frame_estado

    canvas = Canvas(frameclients, bg='white', border=0)
    canvas.pack(expand=True, fill=BOTH, side=LEFT)

    frame_nome = Frame(frameclients, bg='black', border=0)
    frame_nome.place(relwidth=0.4, rely=0, relx=0)
    inicial_nome = Label(frame_nome, text='Nome', font=('arial', 16), bg='white', fg='black')
    inicial_nome.pack(anchor='w', pady=0, fill=X)

    frame_cpf = Frame(frameclients, bg='black', border=0)
    frame_cpf.place(relwidth=0.15, rely=0, relx=0.401)
    inicial_sobrenome = Label(frame_cpf, text='CPF', font=('arial', 16), bg='white', fg='black')
    inicial_sobrenome.pack(anchor='w', pady=0, fill=X)

    frame_cidade = Frame(frameclients, bg='black', border=0)
    frame_cidade.place(relwidth=0.25, rely=0, relx=0.5522)
    inicial_cidade = Label(frame_cidade, text='Cidade', font=('arial', 16), bg='white', fg='black')
    inicial_cidade.pack(anchor='w', pady=0, fill=X)

    frame_estado = Frame(frameclients, bg='black', border=0)
    frame_estado.place(relwidth=0.1945, rely=0, relx=0.804)
    inicial_estado = Label(frame_estado, text='Estado', font=('arial', 16), bg='white', fg='black')
    inicial_estado.pack(anchor='w', pady=0, fill=X)
    
def janela_clientes(frameinfo):

    imports()

    #frame onde mostra o nome dos clientes
    frameclients = Frame(frameinfo, bg='white', border=0)
    frameclients.place(relheight=0.9, relwidth=0.99, rely=0.25, relx=0.005)
    
    #frame onde mostra as opções da lista
    framelist = Frame(frameinfo, bg='white', border=0)
    framelist.place(relheight=0.05, relwidth=1, rely=0.2)

    #frames da tabela
    frame_lista_clientes(frameclients)

    #configurações da janela
    register_button = Button(frameinfo, text='REGISTRAR', font=('arial', 20, 'bold'), bg='white', fg='black', border=0, command=partial(window_register, frame_nome, frame_cpf, frame_cidade, frame_estado))
    register_button.place(y=144, x=530)

    view_client_button = Button(frameinfo, text='VISUALIZAR', font=('arial', 20, 'bold'), bg='white', fg='black', border=0, command=lambda: StartUI())
    view_client_button.place(y=144, x=730)

    client_history = Button(frameinfo, text='HISTÓRICO', font=('arial', 20, 'bold'), bg='white', fg='black', border=0)
    client_history.place(y=144, x=930)

    search_clients = Entry(framelist, font=('arial', 10), bg='white', fg='black')
    search_clients.place(y=10, x=300, width=800, height=30)

    btn_client_search = Button(framelist, text='BUSCAR', font=('arial', 16), bg='green', fg='white', border=0)
    btn_client_search.place(y=10, x=820, width=150, height=30)