from tkinter import *
import os, sys

logic_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(logic_path, 'MensagensInfos'))
from services.MensagensInfos import LogicLog
from database.SoftwareDB import DBLog

def aba_relatorios(frameinfo):
    # Frame principal da aba de relatórios
    main_frame = Frame(frameinfo, bg='white')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Título
    Label(main_frame, text='Relatórios de Movimentação de Estoque',
          font=('Arial', 20, 'bold'), bg=main_frame.cget('bg')).pack(anchor='center', pady=(15, 20))

    # Frame de filtro
    frame_filtro = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_filtro.pack(fill='x', pady=(0, 10))

    Label(frame_filtro, text="Filtrar por Tipo:", font=('Arial', 12), bg=main_frame.cget('bg')).pack(side='left')

    filtro_tipo = StringVar()
    filtro_tipo.set("Todos")
    OptionMenu(frame_filtro, filtro_tipo, "Todos", "Adicionados", "Removidos", "Vendidos", "Estoque Baixo").pack(
        side='left', padx=10)

    Button(frame_filtro, text='Aplicar Filtro', font=('Arial', 11, 'bold'),
           bg='gray', fg='white', cursor='hand2', command=lambda:(LogicLog.GetFilter(filtro_tipo))).pack(side='left', padx=10)

    # Frame de exibição do relatório
    frame_relatorio = Frame(main_frame, bg='white')
    frame_relatorio.pack(fill='both', expand=True)

    scrollbar = Scrollbar(frame_relatorio)
    scrollbar.pack(side='right', fill='y')

    text_relatorio = Text(frame_relatorio, font=('Arial', 12), yscrollcommand=scrollbar.set, wrap='word')
    text_relatorio.pack(fill='both', expand=True)
    scrollbar.config(command=text_relatorio.yview)

    # Exemplo de dados temporários
    dadosLOG = DBLog.LoadLogDB()

    for linha in dadosLOG:
        id_, situacao, nome, marca, quantidade, data = linha
        linha_formatada = (f'| {situacao} |  Produto: {nome} - Marca: {marca} - Quantidade: {int(quantidade)} - Data Inserida: {data}')
        text_relatorio.insert(END, f'\n{linha_formatada}\n')

    text_relatorio.config(state='disabled')