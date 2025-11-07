from tkinter import *
import os, sys

function_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, function_path)
from services.infosmain import Functions
from database.SoftwareDB import DBLog

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

    #Variáveis para registrar informações
    CounterRegisterProdutcs = IntVar(value=Functions().LoadInfosRegistred()) #Valor do contador de produtos registrados
    LowStockProducts = IntVar(value=Functions().LoadAlertRegistred()) #Valor do contador de produtos com estoque baixo
    QuantitySell = IntVar(value=Functions().LoadSellQuantity())
    ##############################################

    # Frame principal
    main_frame = Frame(frameinfo, bg='#f7f9fb')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Título
    Label(main_frame, text='Resumo do Sistema', font=('Arial', 22, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w', pady=(0, 20))

    # Frame de indicadores
    frame_indicadores = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_indicadores.pack(fill='x', pady=10)

    # Produto registrado
    frame_produtos = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_produtos.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_produtos, text='Produtos Registrados', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_produtos, textvariable=CounterRegisterProdutcs, font=('Arial', 16), bg='#f0f0f0', fg='blue').pack(pady=(5, 10))

    # Vendas realizadas
    frame_vendas = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_vendas.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_vendas, text='Vendas Realizadas', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_vendas, textvariable=QuantitySell, font=('Arial', 16), bg='#f0f0f0', fg='green').pack(pady=(5, 10))

    # Estoque baixo
    frame_estoque_baixo = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_estoque_baixo.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_estoque_baixo, text='Estoque Baixo', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_estoque_baixo, textvariable=LowStockProducts, font=('Arial', 16), bg='#f0f0f0', fg='red').pack(pady=(5, 10))

    # Avisos / Notificações
    # Frame de avisos com barra de rolagem
    frame_avisos = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_avisos.pack(fill='both', expand=True, pady=(20, 0))

    Label(frame_avisos, text='Avisos de Produto Baixo:', font=('Arial', 14, 'bold'), bg=main_frame.cget('bg')).pack(
        anchor='w')

    # Frame que segura o canvas e a scrollbar
    frame_canvas = Frame(frame_avisos, bg=main_frame.cget('bg'))
    frame_canvas.pack(fill='both', expand=True)

    # Canvas + Scrollbar
    canvas = Canvas(frame_canvas, bg=main_frame.cget('bg'), highlightthickness=0, bd=0)
    scrollbar = Scrollbar(frame_canvas, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)

    # Frame interno rolável
    scrollable_frame = Frame(canvas, bg=main_frame.cget('bg'))
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    # garante que as dimensões iniciais estejam corretas
    canvas.update_idletasks()

    # Atualiza a área de rolagem quando o conteúdo muda
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Ajusta a largura do frame interno quando o canvas muda
    def on_canvas_configure(event):
        # event.width é a largura atual do canvas visível
        new_width = event.width
        # aplica largura ao objeto window e ao frame (redundância útil)
        canvas.itemconfig(window_id, width=new_width)
        try:
            scrollable_frame.configure(width=new_width)
        except Exception:
            pass

    canvas.bind("<Configure>", on_canvas_configure)

    # Avisos estilizados (usando expand True para forçar ocupação total)

    avisos = logica_principal()

    for texto, bg_color, fg_color in avisos:
        lbl = Label(scrollable_frame, text=texto, font=('Arial', 12), bg=bg_color, fg=fg_color,
                    anchor='w', justify='left', padx=10, pady=6, relief='groove')
        lbl.pack(fill='x', expand=True, pady=4)  # expand=True aqui é importante
