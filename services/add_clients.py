from tkinter import *
from tkinter import messagebox

def config_cpf(getcpf):

    print("Iniciou a configuração do CPF")

    cpf = ''.join(filter(str.isdigit, getcpf))
    print(f"CPF sem formatação: {cpf}")

    cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    print(f"CPF formatado: {cpf}")
    return cpf

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False
    # Verificação dos dígitos verificadores
    def calcular_digito(cpf, peso):
        soma = sum(int(cpf[i]) * peso[i] for i in range(len(peso)))
        digito = 11 - (soma % 11)
        return digito if digito < 10 else 0

    peso1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    peso2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    digito1 = calcular_digito(cpf[:9], peso1)
    digito2 = calcular_digito(cpf[:10], peso2)
    return cpf[-2:] == f"{digito1}{digito2}"


def add_list(janela, frame_nome, entry_name, entry_secname, frame_cpf, entry_cpf, frame_cidade, select_cidade):

    #strinvar
    place_name = StringVar()
    place_cpf = StringVar()

    #pegandos os dados do entry
    getname = entry_name.get()
    getsecname = entry_secname.get()
    getcpf = entry_cpf.get()

    #conferindo se o cpf está válido
    if not validar_cpf(getcpf):
        messagebox.showerror("Erro", "CPF inválido!")
        return

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
