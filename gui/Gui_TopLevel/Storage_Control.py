from tkinter import *

def abrir_gerenciador_estoque():
    janela = Toplevel()
    janela.title("Gerenciar Estoque")
    janela.geometry("500x400")
    janela.configure(bg='white')
    janela.resizable(False, False)

    Label(janela, text="Gerenciar Estoque", font=('Arial', 20, 'bold'), bg='white').pack(pady=15)

    frame_conteudo = Frame(janela, bg='white')
    frame_conteudo.pack(pady=10, padx=20, fill='x')

    # Campo: Código do Produto
    Label(frame_conteudo, text="Código do Produto:", font=('Arial', 12), bg='white').pack(anchor='w')
    entry_codigo = Entry(frame_conteudo, font=('Arial', 12))
    entry_codigo.pack(fill='x', pady=5)

    # Campo: Nome do Produto
    Label(frame_conteudo, text="Nome do Produto:", font=('Arial', 12), bg='white').pack(anchor='w')
    entry_nome = Entry(frame_conteudo, font=('Arial', 12))
    entry_nome.pack(fill='x', pady=5)

    # Campo: Quantidade
    Label(frame_conteudo, text="Quantidade:", font=('Arial', 12), bg='white').pack(anchor='w')
    entry_quantidade = Entry(frame_conteudo, font=('Arial', 12))
    entry_quantidade.pack(fill='x', pady=5)

    # Campo: Preço
    Label(frame_conteudo, text="Preço (R$):", font=('Arial', 12), bg='white').pack(anchor='w')
    entry_preco = Entry(frame_conteudo, font=('Arial', 12))
    entry_preco.pack(fill='x', pady=5)

    # Botões
    frame_botoes = Frame(janela, bg='white')
    frame_botoes.pack(pady=20)

    Button(frame_botoes, text="Adicionar", font=('Arial', 12, 'bold'), width=12,
           bg='green', fg='white', cursor='hand2').grid(row=0, column=0, padx=10)

    Button(frame_botoes, text="Editar", font=('Arial', 12, 'bold'), width=12,
           bg='orange', fg='white', cursor='hand2').grid(row=0, column=1, padx=10)

    Button(frame_botoes, text="Excluir", font=('Arial', 12, 'bold'), width=12,
           bg='red', fg='white', cursor='hand2').grid(row=0, column=2, padx=10)