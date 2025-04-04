from tkinter import *
from tkinter import messagebox

def config_cpf(getcpf):

    print("iniciou a configuração do cpf")

    cpf = ''.join(filter(str.isdigit, getcpf))

    print(f"CPF sem formatação: {cpf}")

    if len(cpf) != 11:
        messagebox.showerror("Erro", "O CPF deve conter 11 dígitos.")
        return False

    cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    print(f"CPF formatado: {cpf}")
    return cpf


def add_list(janela, frame_nome, entry_name, entry_secname, frame_cpf, entry_cpf, frame_cidade, select_cidade):

    #strinvar
    place_name = StringVar()
    place_cpf = StringVar()

    #pegandos os dados do entry
    getname = entry_name.get()
    getsecname = entry_secname.get()
    getcpf = entry_cpf.get()
    getcidade = select_cidade.get()
    
    #adicionando os dados na lista
    place_name.set(f"{getname.upper()} {getsecname.upper()}")
    converted_cpf = config_cpf(getcpf)
    place_cpf.set(converted_cpf)

    add_name = Label(frame_nome, textvariable=place_name, bg='white', fg='black', font=('arial', 16))
    add_name.pack(anchor='w', pady=0.5, fill=X)

    add_cpf = Label(frame_cpf, textvariable=place_cpf, bg='white', fg='black', font=('arial', 16))
    add_cpf.pack(anchor='w', pady=0.5, fill=X)

    add_cidade = Label(frame_cidade, text=getcidade, bg='white', fg='black', font=('arial', 16))
    add_cidade.pack(anchor='w', pady=0.5, fill=X)

    janela.destroy()
