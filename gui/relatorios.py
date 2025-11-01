from tkinter import *
import os, sys

logic_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(logic_path, 'MensagensInfos'))
from services.MensagensInfos import LogicLog
from database.SoftwareDB import DBLog

def logic_relatorio(text_relatorio):
    dadosLOG = DBLog.LoadLogDB()

    for linha in dadosLOG:
        id_, situacao, nome, marca, quantidade, data = linha
        linha_formatada = f'| {situacao} |  Produto: {nome} - Marca: {marca} - Quantidade: {int(quantidade)} - Data Inserida: {data}\n'
        text_relatorio.insert(
            END,
            linha_formatada,
            situacao.lower().replace(' ', '')  # aplica tag de cor automaticamente
        )


def aba_relatorios(frameinfo):
    # ====== FRAME PRINCIPAL ======
    main_frame = Frame(frameinfo, bg='#f9f9f9')
    main_frame.pack(fill='both', expand=True, padx=30, pady=30)

    # ====== CABEÇALHO ======
    header_frame = Frame(main_frame, bg=main_frame.cget('bg'))
    header_frame.pack(fill='x', pady=(0, 20))

    Label(
        header_frame,
        text='📊 Relatórios de Movimentação de Estoque',
        font=('Segoe UI', 20, 'bold'),
        bg=main_frame.cget('bg'),
        fg='#2b2b2b'
    ).pack(anchor='center')

    # ====== FILTROS ======
    filtro_frame = Frame(main_frame, bg='white', highlightbackground='#d0d0d0', highlightthickness=1)
    filtro_frame.pack(fill='x', pady=(0, 15))
    filtro_frame.configure(padx=15, pady=12)

    Label(
        filtro_frame,
        text="Filtrar por Tipo:",
        font=('Segoe UI', 12, 'bold'),
        bg='white',
        fg='#333'
    ).pack(side='left', padx=(0, 8))

    filtro_tipo = StringVar(value="Todos")

    opt = OptionMenu(
        filtro_frame,
        filtro_tipo,
        "Todos", "Adicionados", "Removidos", "Vendidos", "Estoque Baixo"
    )
    opt.config(
        font=('Segoe UI', 11),
        bg='#f0f0f0',
        fg='#000',
        activebackground='#e0e0e0',
        relief='flat',
        width=14,
        highlightthickness=0
    )
    opt.pack(side='left')

    Button(
        filtro_frame,
        text='Aplicar Filtro',
        font=('Segoe UI', 11, 'bold'),
        bg='#0078D7',
        fg='white',
        cursor='hand2',
        relief='flat',
        activebackground='#005A9E',
        activeforeground='white',
        width=14,
        command=lambda: (LogicLog.GetFilter(filtro_tipo))  # mantém tua função
    ).pack(side='left', padx=10)

    # ====== ÁREA DE RELATÓRIOS ======
    container_relatorio = Frame(main_frame, bg='white', highlightbackground='#d0d0d0', highlightthickness=1)
    container_relatorio.pack(fill='both', expand=True)

    # Scrollbar
    scrollbar = Scrollbar(container_relatorio, orient='vertical')
    scrollbar.pack(side='right', fill='y')

    text_relatorio = Text(
        container_relatorio,
        font=('Consolas', 11),
        yscrollcommand=scrollbar.set,
        wrap='word',
        bg='white',
        fg='#333',
        relief='flat',
        padx=15,
        pady=15
    )
    text_relatorio.pack(fill='both', expand=True)
    scrollbar.config(command=text_relatorio.yview)

    # ====== ESTILIZAÇÃO DE TAGS (cores de categorias) ======
    text_relatorio.tag_config('Adicionados', foreground='#1e9c34')
    text_relatorio.tag_config('Removidos', foreground='#d43f3f')
    text_relatorio.tag_config('Vendidos', foreground='#0078D7')
    text_relatorio.tag_config('Estoque Baixo', foreground='#e69800')

    # ====== CARREGAMENTO DOS DADOS DO BANCO ======
    logic_relatorio(text_relatorio)

    text_relatorio.config(state='disabled')

