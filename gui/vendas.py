from tkinter import *

def janela_vendas(frameinfo):

    # Frame principal
    main_frame = Frame(frameinfo, bg='#F8FAFC')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Título
    Label(main_frame, text='Realizar Venda', font=('Arial', 28, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w', pady=(0, 20))

    # Frame - Código do produto
    frame_codigo = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_codigo.pack(fill='x', pady=5)
    Label(frame_codigo, text='Código do Produto:', font=('Arial', 14), bg=main_frame.cget('bg')).pack(side='left')
    Entry(frame_codigo, font=('Arial', 14), border=2).pack(side='left', padx=10, fill='x', expand=True)

    # Frame - Nome do produto
    frame_nome = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_nome.pack(fill='x', pady=5)
    Label(frame_nome, text='Nome:', font=('Arial', 14), bg=main_frame.cget('bg')).pack(side='left')
    Entry(frame_nome, font=('Arial', 14), state='disabled').pack(side='left', padx=61, fill='x', expand=True)

    # Frame - Preço unitário
    frame_preco = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_preco.pack(fill='x', pady=5)
    Label(frame_preco, text='Preço Unitário:', font=('Arial', 14), bg=main_frame.cget('bg')).pack(side='left')
    Entry(frame_preco, font=('Arial', 14), state='disabled').pack(side='left', padx=36, fill='x', expand=True)

    # Frame - Quantidade e botão adicionar
    frame_quantidade = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_quantidade.pack(fill='x', pady=5)
    Label(frame_quantidade, text='Quantidade:', font=('Arial', 14), bg=main_frame.cget('bg')).pack(side='left')
    Entry(frame_quantidade, font=('Arial', 14), width=10).pack(side='left', padx=10)
    Button(frame_quantidade, text='Adicionar à venda', font=('Arial', 14, 'bold'),
           bg='green', fg='white', cursor='hand2').pack(side='left', padx=30)

    # Itens da venda
    Label(main_frame, text='Itens da Venda:', font=('Arial', 16, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w', pady=(20, 5))
    listbox = Listbox(main_frame, font=('Arial', 13))
    listbox.pack(fill='both', expand=True)

    # Frame total e botões
    frame_total = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_total.pack(fill='x', pady=15)
    Label(frame_total, text='TOTAL:', font=('Arial', 18, 'bold'), bg=main_frame.cget('bg')).pack(side='left')
    Entry(frame_total, font=('Arial', 18, 'bold'), state='disabled', justify='center', width=10).pack(side='left', padx=10)
    Button(frame_total, text='Finalizar Venda', font=('Arial', 16, 'bold'),
           bg='green', fg='white', cursor='hand2').pack(side='right', padx=10)
    Button(frame_total, text='Cancelar', font=('Arial', 16, 'bold'),
           bg='red', fg='white', cursor='hand2').pack(side='right')

    # Resumo da venda
    Label(main_frame, text='Resumo da Venda:', font=('Arial', 15, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w', pady=(10, 5))

    frame_resumo = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_resumo.pack(fill='x', pady=5)

    Label(frame_resumo, text='Itens:', font=('Arial', 12), bg=main_frame.cget('bg')).pack(side='left')
    Entry(frame_resumo, font=('Arial', 12), width=5, state='disabled').pack(side='left', padx=5)

    Label(frame_resumo, text='Quantidade Total:', font=('Arial', 12), bg=main_frame.cget('bg')).pack(side='left', padx=10)
    Entry(frame_resumo, font=('Arial', 12), width=7, state='disabled').pack(side='left', padx=5)

    Label(frame_resumo, text='Cliente:', font=('Arial', 12), bg=main_frame.cget('bg')).pack(side='left', padx=10)
    Entry(frame_resumo, font=('Arial', 12), width=25).pack(side='left', padx=5)

    Label(frame_resumo, text='Forma de Pagamento:', font=('Arial', 12), bg=main_frame.cget('bg')).pack(side='left', padx=10)
    pagamento = StringVar(value='Dinheiro')
    OptionMenu(frame_resumo, pagamento, 'Dinheiro', 'Cartão', 'PIX', 'Outro').pack(side='left')

