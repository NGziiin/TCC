import psycopg2, os, hashlib, plyer
from psycopg2 import errors
import datetime
from dotenv import load_dotenv
import tkinter as tk
from gui.Gui_TopLevel import ComprovanteGui
from CTkMessagebox import CTkMessagebox

load_dotenv()

class StorageRegisterClassDB:
    def CreateStorageDB():
        connection = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = connection.cursor()

        #TABELA DE PRODUTO
        cursor.execute('''CREATE TABLE IF NOT EXISTS produto (
                       id SERIAL PRIMARY KEY,
                       nome VARCHAR(100) NOT NULL,
                       descricao TEXT,
                       marca VARCHAR(50),
                       margem_lucro TEXT
                       )''')
        
        #TABELA DE ESTOQUE
        cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                       produto_id INTEGER PRIMARY KEY,
                       qtd_atual INT NOT NULL,
                       valor_venda NUMERIC(10,2),
                       ultimo_valor_pago NUMERIC(10,2),
                       FOREIGN KEY (produto_id) REFERENCES produto(id))
                       ''')
        
        #TABELA DE ENTRADA DE PRODUTO
        cursor.execute('''CREATE TABLE IF NOT EXISTS entrada_produto (
                       id SERIAL PRIMARY KEY,
                       data DATE NOT NULL,
                       descricao TEXT
                       )''')
        
        #TABELA DE ITENS DE ENTRADA
        cursor.execute('''CREATE TABLE IF NOT EXISTS itens_entrada (
                       id_entrada SERIAL PRIMARY KEY,
                       produto_id INT NOT NULL,
                       qtd INT NOT NULL,
                       valor_unitario NUMERIC(10,2),
                       FOREIGN KEY (id_entrada) REFERENCES entrada_produto(id),
                       FOREIGN KEY (produto_id) REFERENCES produto(id))
                       ''')
        
        #TABELA DE VENDA
        cursor.execute('''CREATE TABLE IF NOT EXISTS venda (
                       id VARCHAR(32) PRIMARY KEY,
                       data DATE NOT NULL,
                       valor NUMERIC(10,2),
                       cliente TEXT NOT NULL
                       )''')
        
        #TABELA DE ITENS VENDA
        cursor.execute('''CREATE TABLE IF NOT EXISTS itens_venda (
                       id SERIAL PRIMARY KEY,
                       id_venda VARCHAR(32) NOT NULL,
                       produto TEXT NOT NULL,
                       qtd INT NOT NULL,
                       valor_unitario NUMERIC(10,2), 
                       FOREIGN KEY (id_venda) REFERENCES venda(id)
                       )''')

        cursor.execute('CREATE TABLE IF NOT EXISTS log ( '
                       'id SERIAL PRIMARY KEY,'
                       'tipo TEXT not null,'  # aqui é onde fica armazenado se foi adicionado, removido, estoque baixo etc...
                       'produto TEXT not null,'
                       'marca TEXT not null,'
                       'quantidade NUMERIC(10,2) not null,'
                       'data DATE not null,'
                       'UNIQUE (tipo, produto, marca, quantidade))')
        connection.commit()
        connection.close()

    def LoadStorageDB(listbox, ref):
        connection = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = connection.cursor()
        ### ESSA LÓGICA MATCH É PARA NÃO PRECISAR CRIAR UMA NOVA FUNÇÃO PARA
        ## ALTERAR SOMENTE 1 INFORMAÇÃO QUE É RECEBIDA DO BANCO DE DADOS.
        match ref:
            case 0:
                try:
                    cursor.execute('SELECT produto.id, produto.nome, produto.marca, estoque.qtd_atual, estoque.valor_venda FROM produto JOIN estoque ON produto.id = estoque.produto_id')
                    infos = cursor.fetchall()
                    connection.commit()
                    cursor.close()
                    for linhas in infos:
                        id_, produto, marca, quantidade, preco = linhas
                        #####ESSE IF SERVE PARA CARREGAR A FUNÇÃO MESMO QUE O LISTBOX RETORNE NULO
                        ### PARA EVITAR DA ERRO DE DECLARAÇÃO DE VARIÁVEL
                        #### POIS NEM SEMPRE VAI TER O LISTBOX
                        if listbox is not None:
                            listbox.insert('', 'end', text=f'{id_}', values=(produto, marca, quantidade, f'R$ {preco:,.2f}'.replace('.', ',')))
                        ############################################################################
                        elif listbox is None:
                            return infos
                except errors.UndefinedTable:
                    cursor.close()
                    pass

            case 1:
                try:
                    cursor.execute('SELECT produto.id, produto.nome, produto.marca, estoque.qtd_atual, estoque.ultimo_valor_pago FROM produto JOIN estoque ON produto.id = estoque.produto_id')
                    infos = cursor.fetchall()
                    connection.commit()
                    cursor.close()
                    return infos

                except errors.UndefinedTable:
                    cursor.close()
                    pass


    #nessa parte aqui a pesquisa é pelo botão de pesquisar
    def LoadSearchStorage(entry_info):
        NameSearch = entry_info
        connection = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT produto.id, '
                           'produto.nome, '
                           'produto.marca '
                           'FROM produto '
                           'JOIN estoque '
                           'ON produto.id = estoque.produto_id '
                           'WHERE produto.nome ILIKE %s OR produto.marca ILIKE %s', (f'%{NameSearch}%', f'%{NameSearch}%'))
            infos = cursor.fetchall()
            cursor.close()
            return infos

        except errors.UndefinedTable:
            cursor.close()
            CTkMessagebox(title='erro', message='houve um erro ao abrir o banco de dados', icon='cancel')
            pass

    def LoadInfosSelected(valores):
        nome, marca = valores
        try:
            connection = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
            cursor = connection.cursor()

            ## configurar a lógica para pegar todas as informações exatas no banco de dados

            cursor.execute('SELECT produto.id, '
                           'produto.nome, '
                           'produto.marca, '
                           'produto.margem_lucro, '
                           'estoque.qtd_atual, '
                           'itens_entrada.valor_unitario, '
                           'estoque.valor_venda '
                           'FROM produto '
                           'JOIN estoque ON produto.id = estoque.produto_id '
                           'JOIN itens_entrada ON produto.id = itens_entrada.produto_id '
                           'WHERE produto.nome ILIKE %s AND produto.marca ILIKE %s', (f'%{nome}%', f'%{marca}%'))
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except errors.UndefinedTable:
            cursor.close()

    def AddStorageDB(NameRegister, AmountRegister, PriceRegister, MarcaRegister, MargemRegister, janela):

        Dateregister = datetime.date.today()
        Dateregister = Dateregister.strftime('%d-%m-%Y %H:%M:%S') #SALVA A DATA NO NA TABELA entrada_produto NA COLUNA descrição

        NameRegister = NameRegister.get()
        LogRegister = f'Foi registrado o produto {NameRegister}'
        LogProdutoRegister = f'Foi registrado o produto na data: {Dateregister}' #SALVA O LOG NA TABELA entrada_produto NA COLUNA descrição

        MarcaRegister = MarcaRegister.get()

        AmountRegister = int(AmountRegister.get())

        PriceRegister = float(PriceRegister.get().replace(',', '.'))

        MargemRegister = MargemRegister.get()
        Porcentagem = int(MargemRegister.replace('%', ''))
        lucro = PriceRegister * (Porcentagem / 100)
        ValorVenda = PriceRegister + lucro

        connection = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM produto WHERE nome = %s', (NameRegister, ))
        verify_nome = cursor.fetchone()
        cursor.execute('SELECT id FROM produto WHERE marca = %s', (MarcaRegister, ))
        verify_marca = cursor.fetchone()

        if verify_nome is not None and verify_marca is not None:
            cursor.close()
            CTkMessagebox(title='ERRO', message='Produto já cadastrado no sistema', icon='cancel')
            return
        elif verify_nome is None or verify_marca is None:
            # Inserir na tabela entrada_produto e capturar o id gerado
            cursor.execute('INSERT INTO entrada_produto (data, descricao) VALUES (%s, %s) RETURNING id;', (Dateregister, LogRegister))
            id_entrada = cursor.fetchone()[0]  # Captura o id retornado
            # Inserir na tabela produto
            cursor.execute('INSERT INTO produto (nome, descricao, marca, margem_lucro) VALUES (%s, %s, %s, %s) RETURNING id;', (NameRegister, LogProdutoRegister, MarcaRegister, MargemRegister))
            id_produto = cursor.fetchone()[0]  # Captura o id do produto
            # Inserir na tabela itens_entrada com id_entrada e id_produto
            cursor.execute('INSERT INTO itens_entrada (id_entrada, produto_id, qtd, valor_unitario) VALUES (%s, %s, %s, %s);', (id_entrada, id_produto, AmountRegister, PriceRegister))
            # Inserir na tabela estoque
            cursor.execute('INSERT INTO estoque (produto_id, qtd_atual, valor_venda, ultimo_valor_pago) VALUES (%s, %s, %s, %s);', (id_produto, AmountRegister, ValorVenda, PriceRegister))
            # INSERE NA TABELA LOG
            cursor.execute('INSERT INTO log (tipo, produto, marca, quantidade, data) VALUES (%s, %s, %s, %s, %s);',
                           ('Adicionado', NameRegister, MarcaRegister, AmountRegister, Dateregister))
            connection.commit()
            cursor.close()
            janela.destroy()
            CTkMessagebox(title='SUCESSO', message='Produto registrado com sucesso', icon='check')

class StorageLowLimitDB:
    def __init__(self):
        pass

    def CreateLowLimitDB():
        connection = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lowlimit (
                id SERIAL PRIMARY KEY,
                quantity_limit INTEGER NOT NULL
            )
        ''')
        connection.commit()
        connection.close()

    def AddLowLimitDB(entry_estoque_baixo):
        quantity_limit = int(entry_estoque_baixo.get())
        connection = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = connection.cursor()
        cursor.execute('DELETE FROM lowlimit')  # Remove entradas anteriores
        cursor.execute('INSERT INTO lowlimit (quantity_limit) VALUES (%s)', (quantity_limit,))
        connection.commit()
        cursor.close()

        #CONFIGURANDO A ENTRY PARA FICAR VAZIA APÓS SALVAR
        entry_estoque_baixo.config(fg='#DCDCDC')
        entry_estoque_baixo.master.focus()

        #MOSTRANDO A MENSAGEM DE SUCESSO
        CTkMessagebox(title='SUCESSO', message='Quantidade mínima atualizada com sucesso', icon='check')

    def LoadLowLimitDB(entry_estoque_baixo):
        connection = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = connection.cursor()
        cursor.execute('SELECT quantity_limit FROM lowlimit ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        try:
            if result:
                entry_estoque_baixo.insert(0, result[0])
        except TypeError:
            entry_estoque_baixo.insert(0, '0')

class DBLog:
    def LoadLogDB():
        conn = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM log')
            infos = cursor.fetchall()
            conn.commit()
            cursor.close()
            return infos

        except errors.UndefinedTable:
            conn.close()
            pass

    #VERIFICAR PORQUE ESTÁ DELETANDO OS ADICIONADOS E SUBISTITUINDO PARA OS DE ESTOQUE BAIXO
    def LowStorage():
        data_atual = datetime.date.today()
        data_atual = data_atual.strftime('%d-%m-%Y %H:%M:%S')
        situacao = 'Estoque Baixo'
        conn = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO log (tipo, produto, marca, quantidade, data)
            SELECT %s , p.nome, p.marca, e.qtd_atual, %s
            FROM estoque e
            JOIN produto p ON p.id = e.produto_id
            WHERE e.qtd_atual < (SELECT quantity_limit FROM lowlimit LIMIT 1)
            ON CONFLICT (tipo, produto, marca, quantidade) DO NOTHING;
        """, (situacao, data_atual,))
        cursor.execute('DELETE FROM log '
                       'USING produto p, estoque e '
                       'WHERE p.id = e.produto_id '
                       'AND log.produto = p.nome '
                       'AND log.marca = p.marca '
                       'AND log.quantidade = e.qtd_atual '
                       'AND log.tipo = %s '
                       'AND e.qtd_atual > (SELECT quantity_limit FROM lowlimit LIMIT 1);',
                       (situacao, )
                       )
        conn.commit()
        conn.close()

    def LowCountMain():
        conn = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM log')
        retornoDB = cursor.fetchall()
        conn.commit()
        cursor.close()
        contador = sum(1 for linha in retornoDB if linha[1] == 'Estoque Baixo')
        return contador

class SellDB:
    def __init__(self):
        pass

    def RegisterSell(listbox, Var_TotalVenda, Entry_Name, Var_TotalProdutos, Var_qtdproduto):

        info_venda = listbox.get(0, tk.END)
        cliente = Entry_Name.get()
        data_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info_compactada = SellDB.SaveVariable(info_venda)
        codigovenda = SellDB.CodVendaHash()

        # Calcula valor total
        valor_total = sum(float(produto[3]) * int(produto[4]) for produto in info_compactada)

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()

        # Inserir venda (apenas uma vez)
        cursor.execute("""
            INSERT INTO venda (id, data, valor, cliente)
            VALUES (%s, %s, %s, %s);
        """, (codigovenda, data_atual, valor_total, cliente))

        items = [] # variável para inserir os itens no comprovante

        # Inserir itens (todos com o mesmo id_venda)
        for produto in info_compactada:
            codigo, nome, marca, preco, quantidade = produto # CODIGO = ID DO PRODUTO

            cursor.execute("""
                INSERT INTO itens_venda (id_venda, produto, qtd, valor_unitario)
                VALUES (%s, %s, %s, %s);
            """, (codigovenda, nome, quantidade, preco))
            # INSERINDO NO LOG
            cursor.execute('INSERT INTO log (tipo, produto, marca, quantidade, data) '
                           'VALUES (%s, %s, %s, %s, %s);', ('Vendido', nome, marca, quantidade, data_atual))

            #ATUALIZA A QUANTIDADE DISPONIVEL NO ESTOQUE
            cursor.execute('UPDATE estoque '
                           'SET qtd_atual = qtd_atual - %s '
                           'WHERE produto_id = %s;', (quantidade, codigo, ))

            items.append((nome, int(quantidade), float(preco)))

        conn.commit()
        cursor.close()
        conn.close()
        # NOTIFICAÇÃO CONFIRMANDO A VENDA
        plyer.notification.notify(title='Sucesso!', message='Venda realizada com sucesso', app_name='Controle de estoque TCC & LTDA', timeout=5)
        SellDB.CleanWindowOK(listbox, Var_TotalVenda, Entry_Name, Var_TotalProdutos, Var_qtdproduto)

        # janela do comprovante
        comprovante = ComprovanteGui.InterfaceComprovante(items=items, codigovenda=codigovenda)
        comprovante.run()

    # Função para limpar a janela quando finalizar
    def CleanWindowOK(listbox, Var_TotalVenda, Entry_Name, Var_TotalProdutos, Var_qtdproduto):
        listbox.delete(0, tk.END)
        Var_TotalVenda.set('R$0,00')
        Entry_Name.set('')
        Var_TotalProdutos.set(0)
        Var_qtdproduto.set(0)

    def SaveVariable(info_venda):
        dados = []
        for item in info_venda:
            partes = item.split('|')
            codigo = partes[0].split(':')[1].strip()
            nome = partes[1].split(':')[1].strip()
            marca = partes[2].split(':')[1].strip()
            preco = partes[3].split(':')[1].strip().replace('R$', '').replace(',', '.')
            quantidade = partes[4].split(':')[1].strip()

            dados.append((codigo, nome, marca, preco, quantidade))

        return dados

    def CodVendaHash():
        data_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hash_obj = hashlib.sha256(data_atual.encode())
        cod_venda = hash_obj.hexdigest()[:10]
        return cod_venda

    def LoadSellDB():
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM venda')
        infos = cursor.fetchall()
        conn.commit()
        cursor.close()

        return infos

class EditProduct:
    def __init__(self):
        pass

    def UpdateInDB(VarCod, VarName, VarMarca, VarPreco, VarQTD, MargemRegister, janela):
        #pegando informações das variaveis
        id_objeto = VarCod.get()
        nome = VarName.get()
        marca = VarMarca.get()
        preco_compra = VarPreco.get().replace("R$", "").replace(",", ".") #preço pago pelo produto
        qtd = VarQTD.get()
        margem = MargemRegister.get()
        if margem == "Selecione uma opção":
            CTkMessagebox(title="Erro", message='selecione uma opção de margem de lucro')
            return

        #fazendo as alterações
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM produto '
                       'WHERE nome = %s AND marca = %s AND id != %s'
                       '', (nome, marca, id_objeto))
        exists = cursor.fetchone()
        if exists:
            CTkMessagebox(title='ERRO', message='Esse produto já existe no sistema', icon='cancel')

        porcentagem = int(margem.replace("%", ""))
        lucro = float(preco_compra) * (porcentagem / 100)
        valor_venda = float(preco_compra) + lucro

        cursor.execute("UPDATE produto SET nome = %s, marca = %s, margem_lucro = %s "
                       "WHERE id = %s;",
                       (nome, marca, margem, id_objeto))

        cursor.execute("UPDATE estoque "
                       "SET qtd_atual = %s, valor_venda = %s, ultimo_valor_pago = %s "
                       "WHERE produto_id = %s;"
                       ,(qtd, valor_venda, preco_compra, id_objeto))

        data_log = datetime.date.today().strftime('%d-%m-%Y %H:%M:%S')
        cursor.execute("INSERT INTO log (tipo, produto, marca, quantidade, data) "
                       "VALUES (%s, %s, %s, %s, %s)",
                       ('Atualizado', nome, marca, qtd, data_log))
        conn.commit()
        cursor.close()
        janela.destroy()
        CTkMessagebox(title="SUCESSO", message='Produto atualizado com sucesso', icon="check")

    def DeleteProductDB(VarCod, VarName, VarMarca, VarPreco, VarQTD, MargemRegister, NameRegister, MarcaRegister, AmountRegister, PriceRegister):
        id_produto = VarCod.get()

        if id_produto == "":
            CTkMessagebox(title="erro de preenchimento", message="preencha o campo com o código que deseja ser deletado")
            return

        msg = CTkMessagebox(title='CONFIRMAR!', message="Tem certeza que deseja deletar o produto informado?", icon='warning', option_1='Sim', option_2='Cancelar')
        resposta = msg.get()
        if resposta == 'Sim':
            try:
                connection = psycopg2.connect(
                    host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"),
                    database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD")
                )
                cursor = connection.cursor()
                # Buscar nome e marca para log
                cursor.execute("SELECT nome, marca FROM produto WHERE id = %s", (id_produto,))
                data = cursor.fetchone()

                if data is None:
                    CTkMessagebox(title="ERRO", message="Produto não encontrado.", icon="cancelar")
                    return

                nome, marca = data
                # 1 - Deletar itens_entrada
                cursor.execute("DELETE FROM itens_entrada WHERE produto_id = %s", (id_produto,))

                # 2 - Deletar estoque
                cursor.execute("DELETE FROM estoque WHERE produto_id = %s", (id_produto,))

                # 3 - Deletar produto
                cursor.execute("DELETE FROM produto WHERE id = %s", (id_produto,))

                # 4 - Registrar log
                data_log = datetime.date.today().strftime('%d-%m-%Y %H:%M:%S')
                cursor.execute("""
                    INSERT INTO log (tipo, produto, marca, quantidade, data)
                    VALUES (%s, %s, %s, %s, %s)
                """, ("Excluído", nome, marca, 0, data_log))

                connection.commit()
                cursor.close()
                CTkMessagebox(title="SUCESSO", message="Produto excluído com sucesso.", icon="check")
                VarCod.set("")
                EditProduct.CleanConfirmedConfig(VarCod, VarName, VarMarca, VarPreco, VarQTD, MargemRegister, NameRegister, MarcaRegister, AmountRegister, PriceRegister)

            except Exception as e:
                CTkMessagebox(title="ERRO", message=str(e), icon="cancel")

        if resposta == 'Cancelar':
            VarCod.set("")
            EditProduct.CleanConfirmedConfig(VarCod, VarName, VarMarca, VarPreco, VarQTD, MargemRegister, NameRegister,
                                             MarcaRegister, AmountRegister, PriceRegister)
            return

    def CleanConfirmedConfig(VarCod, VarName, VarMarca, VarPreco, VarQTD, MargemRegister, NameRegister, MarcaRegister, AmountRegister, PriceRegister):
        codigo = VarCod.get()
        if codigo == "":
            VarName.set('')
            VarMarca.set('')
            VarQTD.set('')
            VarPreco.set('')

            # Habilitando para bloquear
            NameRegister.configure(state='disabled', fg_color='#CDC9C9')
            MarcaRegister.configure(state='disabled', fg_color='#CDC9C9')
            AmountRegister.configure(state='disabled', fg_color='#CDC9C9')
            PriceRegister.configure(state='disabled', fg_color='#CDC9C9')
            MargemRegister.set("Selecione uma opção")