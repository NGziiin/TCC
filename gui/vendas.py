from tkinter import *

def janela_vendas(frameinfo):
    # Limpar frame caso tenha algo
    for widget in frameinfo.winfo_children():
        widget.destroy()

    # Título
    titulo = Label(frameinfo, text='Realizar Venda', font=('Arial', 24, 'bold'), bg='white')
    titulo.place(x=30, y=20)

    # Código do produto
    Label(frameinfo, text='Código do Produto:', font=('Arial', 12), bg='white').place(x=30, y=100)
    entry_codigo = Entry(frameinfo, font=('Arial', 12))
    entry_codigo.place(x=180, y=100, width=200)

    # Nome do produto
    Label(frameinfo, text='Nome:', font=('Arial', 12), bg='white').place(x=30, y=150)
    entry_nome = Entry(frameinfo, font=('Arial', 12), state='disabled')
    entry_nome.place(x=180, y=150, width=400)

    # Preço unitário
    Label(frameinfo, text='Preço Unitário:', font=('Arial', 12), bg='white').place(x=30, y=200)
    entry_preco = Entry(frameinfo, font=('Arial', 12), state='disabled')
    entry_preco.place(x=180, y=200, width=200)

    # Quantidade
    Label(frameinfo, text='Quantidade:', font=('Arial', 12), bg='white').place(x=30, y=250)
    entry_quantidade = Entry(frameinfo, font=('Arial', 12))
    entry_quantidade.place(x=180, y=250, width=100)

    # Botão adicionar
    btn_adicionar = Button(frameinfo, text='Adicionar à venda', font=('Arial', 12, 'bold'),
                           bg='green', fg='white', cursor='hand2')
    btn_adicionar.place(x=320, y=250, width=180, height=30)

    # Lista de itens adicionados
    Label(frameinfo, text='Itens da Venda:', font=('Arial', 14, 'bold'), bg='white').place(x=30, y=310)
    listbox = Listbox(frameinfo, font=('Arial', 12))
    listbox.place(x=30, y=340, width=800, height=300)

    # Total
    Label(frameinfo, text='TOTAL:', font=('Arial', 14, 'bold'), bg='white').place(x=900, y=340)
    entry_total = Entry(frameinfo, font=('Arial', 16, 'bold'), state='disabled', justify='center')
    entry_total.place(x=980, y=340, width=200, height=40)

    # Botão Finalizar Venda
    btn_finalizar = Button(frameinfo, text='Finalizar Venda', font=('Arial', 14, 'bold'),
                           bg='green', fg='white', cursor='hand2')
    btn_finalizar.place(x=980, y=420, width=200, height=40)

    # Botão Cancelar
    btn_cancelar = Button(frameinfo, text='Cancelar', font=('Arial', 14, 'bold'),
                          bg='red', fg='white', cursor='hand2')
    btn_cancelar.place(x=980, y=480, width=200, height=40)