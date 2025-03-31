from tkinter import *

def janela_clientes(frameinfo):
    
    framelist = LabelFrame(frameinfo, bg='green', border=0)
    framelist.place(relheight=0.8, relwidth=1, rely=0.2)

    register_button = Button(frameinfo, text='REGISTRAR', font=('arial', 20, 'bold'), bg='white', fg='black', border=0)
    register_button.place(y=144, x=530)

    view_client_button = Button(frameinfo, text='VISUALIZAR', font=('arial', 20, 'bold'), bg='white', fg='black', border=0)
    view_client_button.place(y=144, x=730)

    client_history = Button(frameinfo, text='HISTÓRICO', font=('arial', 20, 'bold'), bg='white', fg='black', border=0)
    client_history.place(y=144, x=930)

    search_clients = Entry(framelist, font=('arial', 20), bg='white', fg='black')
    search_clients.place(y=50, x=0, width=800, height=30)
    search_clients.insert(0, 'BUSCAR CLIENTE')