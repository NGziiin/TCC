from tkinter import *
import os, sys

class ScrollableFrame(Frame):
    def __init__(self, parent, bg=None, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.bg = bg or self.cget('bg')

        # canvas + scrollbar
        self.canvas = Canvas(self, bg=self.bg, highlightthickness=0, bd=0)
        self.vscroll = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)

        self.vscroll.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Frame interno
        self.inner = Frame(self.canvas, bg=self.bg)
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor=NW)

        # binds
        self.inner.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        new_width = event.width

        try:
            sb_width = self.vscroll.winfo_width()
            if sb_width > 0:
                new_width = max(0, new_width - sb_width)
        except:
            pass

        # força o tamanho do frame interno
        self.canvas.itemconfig(self.window_id, width=new_width)
        try:
            self.inner.configure(width=new_width)
        except:
            pass

    def clear(self):
        # remove widgets antigos
        for w in self.inner.winfo_children():
            w.destroy()

        # reseta scroll
        try:
            self.canvas.yview_moveto(0)
        except:
            pass

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


function_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, function_path)
from services.infosmain import Functions
from database.SoftwareDB import DBLog

# IMPORTANTE: ScrollableFrame está ali em cima

def logica_principal():
    dadosLOG = DBLog.LoadLogDB()
    avisos = []
    for linha in dadosLOG:
        id_, situacao, nome, marca, quantidade, data = linha
        if situacao == 'Estoque Baixo':
            texto = f'⚠️ Produto {nome} da marca {marca} está com estoque baixo ({int(quantidade)} unidades).'
            avisos.append((texto, '#f8d7da', 'red'))
    return avisos


def janelainicial(frameinfo):

    # Variáveis
    CounterRegisterProdutcs = IntVar(value=Functions().LoadInfosRegistred())
    LowStockProducts = IntVar(value=Functions().LoadAlertRegistred())
    QuantitySell = IntVar(value=Functions().LoadSellQuantity())

    # Frame principal
    main_frame = Frame(frameinfo, bg='#f7f9fb')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    Label(main_frame, text='Resumo do Sistema', font=('Arial', 22, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w', pady=(0, 20))

    # Indicadores
    frame_indicadores = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_indicadores.pack(fill='x', pady=10)

    # Produto registrado
    frame_produtos = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_produtos.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_produtos, text='Produtos Registrados', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_produtos, textvariable=CounterRegisterProdutcs, font=('Arial', 16), bg='#f0f0f0', fg='blue').pack(pady=(5, 10))

    # Vendas
    frame_vendas = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_vendas.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_vendas, text='Vendas Realizadas', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_vendas, textvariable=QuantitySell, font=('Arial', 16), bg='#f0f0f0', fg='green').pack(pady=(5, 10))

    # Estoque baixo
    frame_estoque_baixo = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_estoque_baixo.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_estoque_baixo, text='Estoque Baixo', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_estoque_baixo, textvariable=LowStockProducts, font=('Arial', 16), bg='#f0f0f0', fg='red').pack(pady=(5, 10))

    # Avisos
    frame_avisos = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_avisos.pack(fill='both', expand=True, pady=(20, 0))

    Label(frame_avisos, text='Avisos de Produto Baixo:', font=('Arial', 14, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w')

    # ScrollableFrame
    scroll = ScrollableFrame(frame_avisos, bg=main_frame.cget('bg'))
    scroll.pack(fill='both', expand=True)

    # Limpa e desenha avisos
    scroll.clear()

    avisos = logica_principal()

    for texto, bg_color, fg_color in avisos:
        lbl = Label(
            scroll.inner,
            text=texto,
            font=('Arial', 12),
            bg=bg_color,
            fg=fg_color,
            anchor='w',
            justify='left',
            padx=10,
            pady=6,
            relief='groove'
        )
        lbl.pack(fill='x', pady=4, padx=4)

    # Ajusta wraplength após layout
    scroll.canvas.update_idletasks()
    largura = scroll.canvas.winfo_width()
    if largura > 50:
        for lbl in scroll.inner.winfo_children():
            lbl.configure(wraplength=largura - 40)

    scroll.canvas.configure(scrollregion=scroll.canvas.bbox("all"))
