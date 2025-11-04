from functools import partial
from tkinter import *
from tkinter import ttk
import sys, os

# --- Imports do sistema ---
gui_topLevel = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(gui_topLevel, 'Gui_TopLevel'))
from Gui_TopLevel import Storage_Control, SearchEstoque

database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')
from database.SoftwareDB import StorageRegisterClassDB, StorageLowLimitDB

# --- Funções auxiliares ---
def change_config_estoque_baixo(event, entry_estoque_baixo):
    entry_estoque_baixo.delete(0, 'end')
    entry_estoque_baixo.config(fg='black')

def block_event(event):
    listbox = event.widget
    if listbox.identify_region(event.x, event.y) == "separator":
        return "break"
    return "break"

def Searching(entry_pesquisa):
    entry_info = entry_pesquisa.get()
    entry_pesquisa.delete(0, 'end')
    SearchEstoque.Interface(entry_info)

# --- Interface principal ---
def janela_estoque(frameinfo):
    # Cores do tema
    COR_FUNDO = "#f7f9fb"
    COR_TITULO = "#212121"
    COR_LARANJA = "#f57c00"
    COR_VERDE = "#2e7d32"
    COR_AZUL = "#1565c0"
    COR_BORDA = "#d9d9d9"

    # Frame principal
    main_frame = Frame(frameinfo, bg=COR_FUNDO)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Título
    Label(
        main_frame,
        text='Controle de Estoque',
        font=('Arial', 24, 'bold'),
        bg=COR_FUNDO,
        fg=COR_TITULO
    ).pack(anchor='w', pady=(0, 20))

    # Frame de pesquisa
    frame_pesquisa = Frame(main_frame, bg=COR_FUNDO)
    frame_pesquisa.pack(fill='x', pady=5)

    Label(
        frame_pesquisa,
        text='Pesquisar Produto:',
        font=('Arial', 12, 'bold'),
        bg=COR_FUNDO,
        fg=COR_TITULO
    ).pack(side='left')

    entry_pesquisa = Entry(
        frame_pesquisa,
        font=('Arial', 12),
        relief='solid',
        bd=1,
        highlightthickness=1,
        highlightbackground=COR_BORDA
    )
    entry_pesquisa.pack(side='left', fill='x', expand=True, padx=10)

    Button(
        frame_pesquisa,
        text='Buscar',
        font=('Arial', 11, 'bold'),
        command=lambda: Searching(entry_pesquisa),
        bg=COR_AZUL,
        fg='white',
        activebackground='#0d47a1',
        activeforeground='white',
        cursor='hand2',
        relief='flat',
        padx=10,
        pady=3
    ).pack(side='left', padx=5)

    Button(
        frame_pesquisa,
        text='Gerenciar Estoque',
        font=('Arial', 11, 'bold'),
        bg=COR_LARANJA,
        fg='white',
        activebackground='#e65100',
        activeforeground='white',
        cursor='hand2',
        relief='flat',
        padx=10,
        pady=3,
        command=partial(Storage_Control.abrir_gerenciador_estoque)
    ).pack(side='left', padx=5)

    # Label da lista
    Label(
        main_frame,
        text='Produtos em Estoque:',
        font=('Arial', 14, 'bold'),
        bg=COR_FUNDO,
        fg=COR_TITULO
    ).pack(anchor='w', pady=(20, 5))

    # Estilo da tabela
    style2 = ttk.Style()
    style2.theme_use('default')
    style2.configure('TABELA1.Treeview.Heading', background='#f2f2f2', font=('Arial', 11, 'bold'))
    style2.configure('TABELA1.Treeview', background='white', foreground='black', rowheight=25)
    style2.map('TABELA1.Treeview', background=[('selected', '#e3f2fd')])

    # Lista de produtos
    listbox = ttk.Treeview(
        main_frame,
        columns=('name', 'marca', 'quantidade', 'price'),
        show='tree headings',
        style='TABELA1.Treeview'
    )

    listbox.heading('#0', text='Código')
    listbox.column('#0', width=70, anchor='center')

    listbox.heading('name', text='Produto')
    listbox.heading('marca', text='Marca')
    listbox.heading('quantidade', text='Quantidade no Estoque')
    listbox.heading('price', text='Valor')

    listbox.column('name', width=250, anchor='center')
    listbox.column('marca', width=220, anchor='center')
    listbox.column('quantidade', width=160, anchor='center')
    listbox.column('price', width=120, anchor='center')

    listbox.pack(fill='both', expand=True, pady=(0, 15))
    listbox.bind("<Button-1>", block_event)

    # Frame do aviso de estoque baixo
    frame_aviso = Frame(main_frame, bg=COR_FUNDO)
    frame_aviso.pack(fill='x', pady=(10, 0))

    Label(
        frame_aviso,
        text='Aviso de Estoque Baixo (Qtd mínima):',
        font=('Arial', 12, 'bold'),
        bg=COR_FUNDO,
        fg=COR_TITULO
    ).pack(side='left')

    entry_estoque_baixo = Entry(
        frame_aviso,
        font=('Arial', 12),
        fg='#9e9e9e',
        relief='solid',
        bd=1,
        width=10
    )
    entry_estoque_baixo.pack(side='left', padx=10)

    Button(
        frame_aviso,
        text='Salvar',
        font=('Arial', 11, 'bold'),
        bg=COR_VERDE,
        fg='white',
        activebackground='#1b5e20',
        activeforeground='white',
        cursor='hand2',
        relief='flat',
        padx=15,
        pady=2,
        command=partial(StorageLowLimitDB.AddLowLimitDB, entry_estoque_baixo)
    ).pack(side='left', padx=(10, 0))

    entry_estoque_baixo.bind('<Button-1>', lambda event: change_config_estoque_baixo(event, entry_estoque_baixo))

    # Carregar dados
    StorageLowLimitDB.LoadLowLimitDB(entry_estoque_baixo)
    StorageRegisterClassDB.LoadStorageDB(listbox)
