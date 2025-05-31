from tkinter import *

def janela_registro_produto(frameinfo):

    # Frame principal que ocupa toda a área disponível
    content = Frame(frameinfo, bg='white')
    content.pack(fill='both', expand=True, padx=20, pady=20)

    # Título
    Label(content, text='Registrar Produto', font=('Arial', 18, 'bold'), bg='white').grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 20))

    def campo(linha, texto, coluna):
        Label(content, text=texto, font=('Arial', 12), bg='white').grid(row=linha, column=coluna*2, sticky='e', padx=5, pady=5)
        entry = Entry(content, font=('Arial', 12))
        entry.grid(row=linha, column=coluna*2 + 1, sticky='we', padx=5, pady=5)
        return entry

    # Campos (duas colunas)
    entry_codigo = campo(1, 'Código:', 0)
    entry_nome = campo(2, 'Nome do Produto:', 0)
    entry_desc = campo(3, 'Descrição:', 0)
    entry_categoria = campo(4, 'Categoria:', 0)

    entry_custo = campo(1, 'Preço de Custo (R$):', 1)
    entry_venda = campo(2, 'Preço de Venda (R$):', 1)
    entry_qtd = campo(3, 'Quantidade Inicial:', 1)

    # Configurar colunas para expandir horizontalmente
    content.columnconfigure(1, weight=1)
    content.columnconfigure(3, weight=1)

    # Botões (em linha)
    botoes = Frame(content, bg='white')
    botoes.grid(row=5, column=0, columnspan=4, sticky='w', pady=20)

    Button(botoes, text='Registrar Produto', font=('Arial', 12), bg='green', fg='white', padx=15).pack(side='left', padx=10)
    Button(botoes, text='Limpar', font=('Arial', 12), bg='gray', fg='white', padx=15).pack(side='left')
