from tkinter import *
from tkinter import messagebox
from database.SoftwareDB import SellDB, StorageRegisterClassDB

# ==================== FUNÇÕES ====================
class Mainbread:
    def AutoAdjust(Entry_Total, Var_TotalVenda):
        texto = Var_TotalVenda.get()
        new_dimension = max(10, len(texto))
        Entry_Total.configure(width=new_dimension)

    def Autopreenchimento(event, Entry_Cod, Var_Name, Var_Preco, Var_Marca):
        global info
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
            Var_Preco.set(f"R${produto['preço']}".replace('.', ','))
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
            preco = 0.00
            quantidade = 0
            partes = item.split('|')
            for parte in partes:
                parte = parte.strip()
                if "Preço:" in parte:
                    try:
                        preco_str = parte.split("Preço:")[1].strip().replace("R$", "").replace(".", 'x').replace(',','.').replace('x', '')
                        preco = float(preco_str)
                    except Exception as e:
                        print(f'erro no preço: {e}')
                if "Quantidade:" in parte:
                    try:
                        qtd_str = parte.split("Quantidade:")[1].strip()
                        quantidade = int(qtd_str)
                    except Exception as e:
                        print(f'erro na quantidade: {e}')
            total += preco * quantidade
        Var_TotalVenda.set(f'R${total:,.2f}'.replace('.', 'x').replace(',', '.').replace('x', ','))

    def Logic(Entry_Cod, Var_Name, Var_Preco, Entry_qtd, listbox, Var_Marca, Var_TotalVenda):
        global info
        getCod = Entry_Cod.get()
        getName = Var_Name.get()
        getPreco = Var_Preco.get()
        getQTD = Entry_qtd.get()
        getMarca = Var_Marca.get()

        if getCod.strip() != '' and getCod is not None and getQTD.strip() != '' and getQTD is not None:
            try:
                qtd_solicitada = int(getQTD)
                estoque = info.get(getCod, {}).get('quantidade', 0)
                if qtd_solicitada > estoque:
                    messagebox.showerror('ESTOQUE INSUFICIENTE',f'Quantidade solicitada ({qtd_solicitada}) maior que o estoque disponível ({estoque})')
                    return

            except ValueError:
                messagebox.showerror('ERRO', 'quantidade inválida')
                return

            listbox.insert(END,f'Código: {getCod} | nome: {getName} - {getMarca} | Preço: {getPreco} | Quantidade: {getQTD}\n')
            Entry_Cod.delete(0, END)
            Entry_qtd.delete(0, END)
            Var_Marca.set('')
            Var_Preco.set('')
            Var_Name.set('')
            Mainbread.Calculo_total(listbox, Var_TotalVenda)
        else:
            messagebox.showerror('FALTA DE INFORMAÇÕES', 'TODOS OS CAMPOS PRECISAM ESTAR PREENCHIDOS')

# ==================== INTERFACE ====================
def janela_vendas(frameinfo):

    # Cores
    CORES = {
        "fundo": "#f7f9fb",
        "verde": "#2E7D32",
        "vermelho": "#C62828",
        "cinza": "#dfe6e9",
        "texto": "#212121",
        "adicionar": "#43a047"
    }

    Var_Name = StringVar()
    Var_Preco = StringVar()
    Var_Marca = StringVar()
    Var_TotalVenda = StringVar(value='R$0,00')

    # Frame principal
    main_frame = Frame(frameinfo, bg=CORES["fundo"])
    main_frame.pack(fill='both', expand=True, padx=25, pady=20)

    Label(main_frame, text='Realizar Venda', font=('Arial', 26, 'bold'), bg=CORES["fundo"], fg=CORES["texto"]).pack(anchor='w', pady=(0, 15))

    # ---------- FRAME PRODUTO ----------
    frame_produto = Frame(main_frame, bg=CORES["fundo"])
    frame_produto.pack(fill='x', pady=10)

    Label(frame_produto, text="Código:", font=('Arial', 12), bg=CORES["fundo"]).grid(row=0, column=0, sticky='w')
    Entry_Cod = Entry(frame_produto, font=('Arial', 12), width=15, relief='flat', highlightthickness=1, highlightbackground=CORES["cinza"])
    Entry_Cod.grid(row=0, column=1, padx=5)
    Entry_Cod.bind("<KeyRelease>", lambda event: Mainbread.Autopreenchimento(event, Entry_Cod, Var_Name, Var_Preco, Var_Marca))

    Label(frame_produto, text="Nome:", font=('Arial', 12), bg=CORES["fundo"]).grid(row=0, column=2, sticky='w', padx=(20,0))
    Entry(frame_produto, textvariable=Var_Name, font=('Arial', 12), state='disabled', width=30,
          relief='flat', disabledbackground=CORES["cinza"]).grid(row=0, column=3, padx=5)

    Label(frame_produto, text="Preço:", font=('Arial', 12), bg=CORES["fundo"]).grid(row=0, column=4, sticky='w', padx=(20,0))
    Entry(frame_produto, textvariable=Var_Preco, font=('Arial', 12), state='disabled', width=10,
          relief='flat', disabledbackground=CORES["cinza"]).grid(row=0, column=5, padx=5)

    Label(frame_produto, text="Qtd:", font=('Arial', 12), bg=CORES["fundo"]).grid(row=0, column=6, sticky='w', padx=(20,0))
    Entry_qtd = Entry(frame_produto, font=('Arial', 12), width=7, relief='flat', highlightthickness=1, highlightbackground=CORES["cinza"])
    Entry_qtd.grid(row=0, column=7, padx=5)

    Button(frame_produto, text="Adicionar", bg=CORES["adicionar"], fg='white', font=('Arial', 12, 'bold'),
           relief='flat', cursor='hand2',
           command=lambda: Mainbread.Logic(Entry_Cod, Var_Name, Var_Preco, Entry_qtd, listbox, Var_Marca, Var_TotalVenda)).grid(row=0, column=8, padx=(20,0))

    # ---------- LISTA DE ITENS ----------
    Label(main_frame, text="Itens da Venda:", font=('Arial', 16, 'bold'), bg=CORES["fundo"], fg=CORES["texto"]).pack(anchor='w', pady=(20, 5))
    frame_lista = Frame(main_frame, bg=CORES["fundo"])
    frame_lista.pack(fill='both', expand=True)

    scroll = Scrollbar(frame_lista)
    scroll.pack(side='right', fill='y')

    listbox = Listbox(frame_lista, font=('Consolas', 12), yscrollcommand=scroll.set, selectmode=SINGLE, relief='flat', bd=1)
    listbox.pack(fill='both', expand=True)
    scroll.config(command=listbox.yview)

    # ---------- RODAPÉ ----------
    frame_footer = Frame(main_frame, bg=CORES["fundo"])
    frame_footer.pack(fill='x', pady=15)

    Label(frame_footer, text='TOTAL:', font=('Arial', 18, 'bold'), bg=CORES["fundo"]).pack(side='left')
    Entry_Total = Entry(frame_footer, font=('Arial', 18, 'bold'), state='disabled', justify='center',
                        textvariable=Var_TotalVenda, width=10, relief='flat', disabledbackground=CORES["cinza"])
    Entry_Total.pack(side='left', padx=10)
    Var_TotalVenda.trace_add('write', lambda n, i, m: Mainbread.AutoAdjust(Entry_Total, Var_TotalVenda))

    Button(frame_footer, text='Finalizar Venda', font=('Arial', 14, 'bold'),
           bg=CORES["verde"], fg='white', cursor='hand2', relief='flat').pack(side='right', padx=5)
    Button(frame_footer, text='Cancelar', font=('Arial', 14, 'bold'),
           bg=CORES["vermelho"], fg='white', cursor='hand2', relief='flat').pack(side='right', padx=5)

    # ---------- RESUMO ----------
    Label(main_frame, text='Resumo da Venda:', font=('Arial', 15, 'bold'), bg=CORES["fundo"], fg=CORES["texto"]).pack(anchor='w', pady=(10, 5))
    frame_resumo = Frame(main_frame, bg=CORES["fundo"])
    frame_resumo.pack(fill='x', pady=5)

    Label(frame_resumo, text='Itens:', bg=CORES["fundo"]).grid(row=0, column=0)
    Entry(frame_resumo, width=5, state='disabled', relief='flat', disabledbackground=CORES["cinza"]).grid(row=0, column=1, padx=5)

    Label(frame_resumo, text='Qtd Total:', bg=CORES["fundo"]).grid(row=0, column=2, padx=(15,0))
    Entry(frame_resumo, width=6, state='disabled', relief='flat', disabledbackground=CORES["cinza"]).grid(row=0, column=3, padx=5)

    Label(frame_resumo, text='Cliente:', bg=CORES["fundo"]).grid(row=0, column=4, padx=(15,0))
    Entry(frame_resumo, width=25, relief='flat', highlightthickness=1, highlightbackground=CORES["cinza"]).grid(row=0, column=5, padx=5)

    Label(frame_resumo, text='Pagamento:', bg=CORES["fundo"]).grid(row=0, column=6, padx=(15,0))
    pagamento = StringVar(value='Dinheiro')
    OptionMenu(frame_resumo, pagamento, 'Dinheiro', 'Cartão', 'PIX').grid(row=0, column=7, padx=5)
