from tkinter import *
from tkinter import messagebox
from database.SoftwareDB import SellDB, StorageRegisterClassDB

def AutoAdjust(Entry_Total, Var_TotalVenda):
    texto = Var_TotalVenda.get()
    new_dimension = max(10, len(texto))
    Entry_Total.configure(width=new_dimension)

def Autopreenchimento(event, Entry_Cod, Var_Name, Var_Preco, Var_Marca):
    codigo = Entry_Cod.get()
    banco_dados = StorageRegisterClassDB.LoadStorageDB(listbox=None)
    info = {}
    for linha in banco_dados:
        id_produto = str(linha[0])
        nome = linha[1]
        marca = linha[2]
        quantidade = linha[3]
        preco = linha[4]

        info[id_produto] = {
            "nome": nome,
            "marca": marca,
            "quantidade": quantidade,
            "preço": preco
        }
    produto = info.get(codigo)
    if produto:
        Var_Name.set(produto['nome'])
        Var_Preco.set(f'R${produto['preço']}'.replace('.', ','))
        Var_Marca.set(produto['marca'])
    elif codigo == '':
        Var_Name.set('')
        Var_Preco.set('')
        Var_Marca.set('')
    else:
        Var_Name.set('Não encontrado')
        Var_Preco.set('-----')
        Var_Marca.set('')

def Calculo_total(listbox, Var_TotalVenda):
    total = 0.00

    for item in listbox.get(0, END):
        preco = 0.0
        quantidade = 0
        partes = item.split('|')
        for parte in partes:
            parte = parte.strip()
            if "Preço:" in parte:
                try:
                    preco_str = parte.split("Preço:")[1].strip().replace("R$", "").replace(".", 'x').replace(',', '.').replace('x', '')
                    preco = float(preco_str)
                except Exception as e:
                    print(f'erro no preço: {e}')

            if "Quantidade:" in parte:
                try:
                    qtd_str = parte.split("Quantidade:")[1].strip()
                    quantidade = int(qtd_str)
                except Exception as e:
                    print(f'erro na quantidade: {e}')

        calculo = preco * quantidade
        total += calculo

    Var_TotalVenda.set(f'R${total:,.2f}'.replace('.', 'x').replace(',', '.').replace('x', ','))

def Logic(Entry_Cod, Var_Name, Var_Preco, Entry_qtd, listbox, Var_Marca, Var_TotalVenda):
    getCod = Entry_Cod.get()
    getName = Var_Name.get()
    getPreco = Var_Preco.get()
    getQTD = Entry_qtd.get()
    getMarca = Var_Marca.get()

    if getCod.strip() != '' and getCod is not None and getQTD.strip() != '' and getQTD is not None:
        #insere na tela para realizar a venda
        listbox.insert(END, f'Código: {getCod} | nome: {getName}  - {getMarca} | Preço: {getPreco} | Quantidade: {getQTD}\n')
        Entry_Cod.delete(0, END)
        Entry_qtd.delete(0, END)
        Var_Marca.set('')
        Var_Preco.set('')
        Var_Name.set('')
        Calculo_total(listbox, Var_TotalVenda)

    else:
        messagebox.showerror('FALTA DE INFORMAÇÕES', 'TODOS OS CAMPOS PRECISAM ESTAR PREENCHIDOS')

def janela_vendas(frameinfo):

    Var_Name = StringVar()
    Var_Preco = StringVar()
    Var_Marca = StringVar()
    Var_TotalVenda = StringVar()
    Var_TotalVenda.set(f'R${0.00}'.replace('.', ','))

    # Frame principal
    main_frame = Frame(frameinfo, bg='white')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Título
    Label(main_frame, text='Realizar Venda', font=('Arial', 28, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w', pady=(0, 20))

    # Frame - Código do produto
    frame_codigo = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_codigo.pack(fill='x', pady=5)
    Label(frame_codigo, text='Código do Produto:', font=('Arial', 14), bg=main_frame.cget('bg')).pack(side='left')
    Entry_Cod = Entry(frame_codigo, font=('Arial', 14), border=2)
    Entry_Cod.pack(side='left', padx=10, fill='x', expand=True)
    Entry_Cod.bind("<KeyRelease>", lambda event: Autopreenchimento(event, Entry_Cod, Var_Name, Var_Preco, Var_Marca))

    # Frame - Nome do produto
    frame_nome = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_nome.pack(fill='x', pady=5)
    Label(frame_nome, text='Nome:', font=('Arial', 14), bg=main_frame.cget('bg')).pack(side='left')
    Entry_Name = Entry(frame_nome, font=('Arial', 14), state='disabled', textvariable=Var_Name).pack(side='left', padx=61, fill='x', expand=True)

    # Frame - Preço unitário
    frame_preco = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_preco.pack(fill='x', pady=5)
    Label(frame_preco, text='Preço Unitário:', font=('Arial', 14), bg=main_frame.cget('bg')).pack(side='left')
    Entry_Preco = Entry(frame_preco, font=('Arial', 14), state="disabled", textvariable=Var_Preco).pack(side='left', padx=36, fill='x', expand=True)

    # Frame - Quantidade e botão adicionar
    frame_quantidade = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_quantidade.pack(fill='x', pady=5)
    Label(frame_quantidade, text='Quantidade:', font=('Arial', 14), bg=main_frame.cget('bg')).pack(side='left')
    Entry_qtd = Entry(frame_quantidade, font=('Arial', 14), width=10)
    Entry_qtd.pack(side='left', padx=10)
    Button(frame_quantidade, text='Adicionar à venda', font=('Arial', 14, 'bold'),
           bg='green', fg='white', cursor='hand2', command=lambda: Logic(Entry_Cod, Var_Name, Var_Preco, Entry_qtd, listbox, Var_Marca, Var_TotalVenda)).pack(side='left', padx=30)

    # Itens da venda
    Label(main_frame, text='Itens da Venda:', font=('Arial', 16, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w',pady=(20, 5))
    listbox = Listbox(main_frame, font=('Arial', 13))
    listbox.pack(fill='both', expand=True)

    # Frame total e botões
    frame_total = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_total.pack(fill='x', pady=15)
    Label(frame_total, text='TOTAL:', font=('Arial', 18, 'bold'), bg=main_frame.cget('bg')).pack(side='left')

    Entry_Total = Entry(frame_total, font=('Arial', 18, 'bold'), state='disabled', justify='center', textvariable=Var_TotalVenda, width=10)
    Entry_Total.pack(side='left', padx=10)

    #aumenta o campo sempre que o valor aumentar
    Var_TotalVenda.trace_add('write', lambda name, index, mode: AutoAdjust(Entry_Total, Var_TotalVenda))

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
    OptionMenu(frame_resumo, pagamento, 'Dinheiro', 'Cartão', 'PIX').pack(side='left')

