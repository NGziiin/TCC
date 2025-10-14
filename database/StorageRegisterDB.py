from multiprocessing.forkserver import connect_to_new_process

import psycopg2
from psycopg2 import errors
import messagebox, datetime

class StorageRegisterClassDB:
    def __init__(self):
        pass

    def CreateStorageDB():
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
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
                       id SERIAL PRIMARY KEY,
                       data DATE NOT NULL,
                       valor NUMERIC(10,2)
                       )''')
        
        #TABELA DE ITENS VENDA
        cursor.execute('''CREATE TABLE IF NOT EXISTS itens_venda (
                       id SERIAL PRIMARY KEY,
                       id_venda INT NOT NULL,
                       produto_id INT NOT NULL,
                       qtd INT NOT NULL,
                       valor_unitario NUMERIC(10,2),
                       FOREIGN KEY (id_venda) REFERENCES venda(id),
                       FOREIGN KEY (produto_id) REFERENCES produto(id)
                       )''')
        connection.commit()
        connection.close()

    def LoadStorageDB(listbox):
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT produto.id, produto.nome, estoque.qtd_atual, estoque.valor_venda FROM produto JOIN estoque ON produto.id = estoque.produto_id')
            infos = cursor.fetchall()
            connection.commit()
            cursor.close()
            for linhas in infos:
                id_, produto, quantidade, preco = linhas
                #####ESSE IF SERVE PARA CARREGAR A FUNÇÃO MESMO QUE O LISTBOX RETORNE NULO
                ### PARA EVITAR DA ERRO DE DECLARAÇÃO DE VARIÁVEL
                #### POIS NEM SEMPRE VAI TER O LISTBOX
                if listbox is not None:
                    listbox.insert('', 'end', text=f'{id_}', values=(produto, quantidade, f'R$ {preco:,.2f}'.replace('.', ',')))
                    ############################################################################
                elif listbox is None:
                    return infos
                             
        except errors.UndefinedTable:
            cursor.close()
            pass


    #nessa parte aqui a pesquisa é pelo botão de pesquisar
    def LoadSearchStorage():
        connection = psycopg2.connect(host='localhost', port='5500', database='postgres', user='postgres', password='2004')
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT produto.id, produto.nome, produto.marca FROM produto JOIN estoque ON produto.id = estoque.produto_id')
            infos = cursor.fetchall()
            cursor.close()
            return infos

        except errors.UndefinedTable:
            cursor.close()
            messagebox.showerror('erro', 'houve um erro ao abrir o banco de dados')
            pass

    def LoadInfosSelected(valores):
        nome, marca = valores
        try:
            connection = psycopg2.connect(host='localhost', port='5500', database='postgres', user='postgres', password='2004')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM produto WHERE nome ILIKE %s AND marca ILIKE %s', (f'%{nome}%', f'%{marca}%'))
            resultado = cursor.fetchall()
            cursor.close()
            print(resultado)
        except errors.UndefinedTable:
            cursor.close()

    def AddStorageDB(NameRegister, AmountRegister, PriceRegister, MarcaRegister, MargemRegister, janela):

        Dateregister = datetime.date.today()
        Dateregister = Dateregister.strftime('%d-%m-%Y') #SALVA A DATA NO NA TABELA entrada_produto NA COLUNA descrição

        NameRegister = NameRegister.get()
        LogRegister = f'Foi registrado o produto {NameRegister}'
        LogProdutoRegister = f'Foi registrado o produto na data: {Dateregister}' #SALVA O LOG NA TABELA entrada_produto NA COLUNA descrição

        MarcaRegister = MarcaRegister.get()

        AmountRegister = int(AmountRegister.get())

        PriceRegister = float(PriceRegister.get().replace(',', '.'))
        print(f'tipo: {type(PriceRegister)} variável:{PriceRegister}')

        MargemRegister = MargemRegister.get()
        Porcentagem = int(MargemRegister.replace('%', ''))
        lucro = PriceRegister * (Porcentagem / 100)
        ValorVenda = PriceRegister + lucro

        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM produto WHERE nome = %s', (NameRegister, ))
        verify_nome = cursor.fetchone()
        cursor.execute('SELECT id FROM produto WHERE marca = %s', (MarcaRegister, ))
        verify_marca = cursor.fetchone()

        if verify_nome is not None and verify_marca is not None:
            cursor.close()
            messagebox.showerror('ERRO', 'Produto já cadastrado no sistema')
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
            connection.commit()
            cursor.close()
            janela.destroy()
            messagebox.showinfo('SUCESSO', 'Produto registrado com sucesso')

class StorageLowLimitDB:
    def __init__(self):
        pass

    def CreateLowLimitDB():
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
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
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
        cursor = connection.cursor()
        cursor.execute('DELETE FROM lowlimit')  # Remove entradas anteriores
        cursor.execute('INSERT INTO lowlimit (quantity_limit) VALUES (%s)', (quantity_limit,))
        connection.commit()
        cursor.close()

        #CONFIGURANDO A ENTRY PARA FICAR VAZIA APÓS SALVAR
        entry_estoque_baixo.config(fg='#DCDCDC')
        entry_estoque_baixo.master.focus()

        #MOSTRANDO A MENSAGEM DE SUCESSO
        messagebox.showinfo('SUCESSO', 'Quantidade mínima atualizada com sucesso')

    def LoadLowLimitDB(entry_estoque_baixo):
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
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