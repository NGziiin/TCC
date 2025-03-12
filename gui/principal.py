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
    canvas_widget.place(x=200, y=350)

    clientes = LabelFrame(frameinfo, bg='white', border=2)
    clientes.place(relheight=0.3, relwidth=0.5, x=200, y=200)