from functools import partial
from tkinter import *
from tkinter import ttk, Tk
import sys
import os

gui_topLevel = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(gui_topLevel, 'Gui_TopLevel'))
from Gui_TopLevel import Storage_Control

def janela_estoque(frameinfo):

    # Frame principal de tudo
    main_frame = Frame(frameinfo, bg='white')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Título
    Label(main_frame, text='Controle de Estoque', font=('Arial', 24, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w', pady=(0, 20))

    # Frame de pesquisa
    frame_pesquisa = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_pesquisa.pack(fill='x', pady=5)

    Label(frame_pesquisa, text='Pesquisar Produto:', font=('Arial', 12), bg=main_frame.cget('bg')).pack(side='left')
    entry_pesquisa = Entry(frame_pesquisa, font=('Arial', 12))
    entry_pesquisa.pack(side='left', fill='x', expand=True, padx=10)
    Button(frame_pesquisa, text='Buscar', font=('Arial', 11, 'bold'), bg='gray', fg='white', cursor='hand2').pack(
        side='left', padx=5)

    # Botão para abrir o gerenciador de estoque
    Button(frame_pesquisa, text='Gerenciar Estoque', font=('Arial', 11, 'bold'), bg='blue',
           fg='white', cursor='hand2', command= partial(Storage_Control.abrir_gerenciador_estoque)).pack(side='left', padx=5)

    # Label da lista
    Label(main_frame, text='Produtos em Estoque:', font=('Arial', 14, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w',
                                                                                                pady=(20, 5))

    # Lista de produtos
    listbox = ttk.Treeview(main_frame, columns=('name', 'quantidade', 'price'), show='headings')
    
    # Configuração das colunas
    listbox.heading('name', text='Produto')
    listbox.heading('quantidade', text='Quantidade no Estoque')
    listbox.heading('price', text='Valor')
    
    listbox.column('name', width=200, anchor='w')
    listbox.column('quantidade', width=150, anchor='center')
    listbox.column('price', width=100, anchor='e')
    
    # Adicionando coluna #0 para o código
    listbox['show'] = 'tree headings'
    listbox.heading('#0', text='Código')
    listbox.column('#0', width=80, anchor='center')
    
    # Inserindo dados de exemplo
    listbox.insert('', 'center', text='001', values=('CAFÉ', 20, 'R$ 15,00'))
    listbox.insert('', 'center', text='002', values=('AÇÚCAR', 35, 'R$ 4,50'))
    listbox.insert('', 'center', text='003', values=('LEITE', 12, 'R$ 6,80'))

    listbox.pack(fill='both', expand=True)

    # Frame de atualização de estoque
    frame_estoque = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_estoque.pack(fill='x', pady=15)

    # Frame do aviso de estoque baixo
    frame_aviso = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_aviso.pack(fill='x')

    Label(frame_aviso, text='Aviso de Estoque Baixo (Qtd mínima):', font=('Arial', 12), bg=main_frame.cget('bg')).pack(side='left')
    entry_estoque_baixo = Entry(frame_aviso, font=('Arial', 12))
    entry_estoque_baixo.pack(side='left', padx=10)
    Button(frame_aviso, text='Salvar', font=('Arial', 12, 'bold'),
           bg='green', fg='white', cursor='hand2').pack(side='left', padx=(10, 0))
