from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import *

def janelainicial(frameinfo):
    welcome = Label(frameinfo, text='Bem Vindo(a) ao Software', font=('arial', 30, 'bold'), bg=frameinfo.cget('bg'))
    welcome.pack(padx=5, pady=50)
    resume = Label(frameinfo, text='RESUMO', font=('arial', 20, 'bold'), bg=frameinfo.cget('bg'))
    resume.pack(padx=5, pady=100)

    fig, ax = plt.subplots(figsize=(4,3), layout='constrained')
    data_atual = datetime.now()
    datas = [data_atual.strftime('%d/%m/%Y')]
    print(datas)
    ax.bar(datas, np.random.rand(len(datas)))
    ax.set_title("GRÁFICO DE VENDAS")

    canvas = FigureCanvasTkAgg(fig, master=frameinfo)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=150, y=350)

    clientes = LabelFrame(frameinfo, bg='white', border=2)
    clientes.place(relheight=0.26, relwidth=0.22, x=630, y=370)

    text_clientes = Label(clientes, text='CLIENTES', font=('arial', 20, 'bold'), bg=clientes.cget('bg'))
    text_clientes.pack(anchor='center')

    clientes_count = StringVar()
    clientes_count.set(2)
    clientes_quantidade = Label(clientes, textvariable=clientes_count, font=('arial', 100, 'bold'), bg=clientes.cget('bg'))
    clientes_quantidade.pack(anchor='center', pady=10)

    produtos = LabelFrame(frameinfo, bg=clientes.cget('bg'), border=2)
    produtos.place(relheight=0.26, relwidth=0.22, x=1060, y=370)

    text_produtos = Label(produtos, text='PRODUTOS REGISTRADOS', font=('arial', 18, 'bold'), bg=produtos.cget('bg'))
    text_produtos.pack(anchor='center')

    produtos_count = StringVar()
    produtos_count.set('40 Mil')
    produtos_quantidade = Label(produtos, textvariable=produtos_count, font=('arial', 75, 'bold'), bg=produtos.cget('bg'))
    produtos_quantidade.pack(anchor='center', pady=35)