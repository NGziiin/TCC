from tkinter import *

def add_list(janela, frame_nome, entry_name, entry_secname, frame_sobrenome):

    #strinvar
    place_name = StringVar()
    place_secname = StringVar()

    #pegandos os dados do entry
    getname = entry_name.get()
    getsecname = entry_secname.get()
    
    #adicionando os dados na lista
    place_name.set(f"{getname.upper()} {getsecname.upper()}")

    add_name = Label(frame_nome, textvariable=place_name, bg='white', fg='black', font=('arial', 16))
    add_name.pack(anchor='w', pady=0.5, fill=X)

    janela.destroy()
