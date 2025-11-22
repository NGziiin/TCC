from database.SoftwareDB import StorageRegisterClassDB

class LogicProduto:
    def autopreenchimento(event, VarCod, VarName, VarMarca, VarPreco, VarQTD, NameRegister, MarcaRegister, AmountRegister, PriceRegister):
        codigo = VarCod.get()
        banco_dados = StorageRegisterClassDB.LoadStorageDB(listbox=None, ref=1, reloadTreeview=1) #a variável Ref é para selecionar diferente no banco de dados
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
            VarName.set(produto['nome'])
            VarMarca.set(produto['marca'])
            VarQTD.set(int(produto['quantidade']))
            VarPreco.set(f"R${produto['preço']}".replace('.', ','))

            #Habilitando para poder editar
            NameRegister.configure(state='normal', fg_color='white')
            MarcaRegister.configure(state='normal', fg_color='white')
            AmountRegister.configure(state='normal', fg_color='white')
            PriceRegister.configure(state='normal', fg_color='white')

        elif codigo == "":
            VarName.set('')
            VarMarca.set('')
            VarQTD.set('')
            VarPreco.set('')

            #Habilitando para bloquear
            NameRegister.configure(state='disabled', fg_color='#CDC9C9')
            MarcaRegister.configure(state='disabled', fg_color='#CDC9C9')
            AmountRegister.configure(state='disabled', fg_color='#CDC9C9')
            PriceRegister.configure(state='disabled', fg_color='#CDC9C9')

        else:
            VarName.set('Não encontrado')
            VarMarca.set('-' * 10)
            VarQTD.set('-' * 10)
            VarPreco.set('-' * 10)

            # Habilitando para bloquear
            NameRegister.configure(state='disabled', fg_color='#CDC9C9')
            MarcaRegister.configure(state='disabled', fg_color='#CDC9C9')
            AmountRegister.configure(state='disabled', fg_color='#CDC9C9')
            PriceRegister.configure(state='disabled', fg_color='#CDC9C9')