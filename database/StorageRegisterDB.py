import psycopg2
from psycopg2 import errors
from tkinter import ttk
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
                       margem_lucro NUMERIC(5,2)
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
            cursor.execute('SELECT * FROM estoque')
            infos = cursor.fetchall()
            connection.commit()
            cursor.close()
            for linhas in infos:
                id_, cod, produto, quantidade, preco = linhas
                #####ESSE IF SERVE PARA CARREGAR A FUNÇÃO MESMO QUE O LISTBOX RETORNE NULO 
                ### PARA EVITAR DA ERRO DE DECLARAÇÃO DE VARIÁVEL 
                #### POIS NEM SEMPRE VAI TER O LISTBOX
                if listbox is not None: 
                    listbox.insert('', 'end', text=f'{cod}', values=(produto, quantidade, f'R$ {preco:,.2f}'.replace('.', ',')))
                    ############################################################################
                elif listbox is None:
                    resultados = []
                    for linhas in infos:
                        resultados.append(linhas)
                        return resultados
                             
        except errors.UndefinedTable:
            cursor.close()
            pass

    def AutomaticUpdateStorageDB():
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
        cursor = connection.cursor()
        cursor.execute('UPDATE produto p SET descricao = ep.descricao FROM itens_entrada ie JOIN entrada_produto ep ON ep.id = ie.id_entrada WHERE p.id = ie.produto_id;')
        connection.commit()
        cursor.close()

    def AddStorageDB(NameRegister, AmountRegister, PriceRegister, MarcaRegister, janela):
        Dateregister = datetime.date.today()
        Dateregister = Dateregister.strftime('%d-%m-%Y') #SALVA A DATA NO NA TABELA entrada_produto NA COLUNA descrição
        NameRegister = NameRegister.get()
        LogRegister = f'Foi registrado o produto {NameRegister}'
        LogProdutoRegister = f'Foi registrado o produto na data: {Dateregister}' #SALVA O LOG NA TABELA entrada_produto NA COLUNA descrição
        MarcaRegister = MarcaRegister.get()
        AmountRegister = int(AmountRegister.get())
        PriceRegister = float(PriceRegister.get().replace(',', '.'))
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO entrada_produto (data, descricao) VALUES (%s, %s) RETURNING id;', (Dateregister, LogRegister)) #INSERE NA TABELA entrada_produto A DATA E O LOG
        cursor.execute('INSERT INTO produto (nome, descricao, marca) VALUES (%s, %s, %s)', (NameRegister, LogProdutoRegister, MarcaRegister)) #INSERE NA TABELA itens_entrada O ID DA ENTRADA, O ID DO PRODUTO, A QUANTIDADE E O VALOR UNITÁRIO
        cursor.execute('INSERT INTO itens_entrada (produto_id, qtd) SELECT id, %s FROM produto RETURNING produto_id, qtd;', (AmountRegister,)) #INSERE NA TABELA estoque O ID DO PRODUTO E A QUANTIDADE ATUAL
        cursor.execute('INSERT INTO estoque (produto_id, qtd_atual, valor_venda, ultimo_valor_pago) SELECT id, %s, %s * 1.30, %s FROM produto ON CONFLICT (produto_id) DO UPDATE SET qtd_atual = estoque.qtd_atual + EXCLUDED.qtd_atual, valor_venda = EXCLUDED.valor_venda, ultimo_valor_pago = EXCLUDED.ultimo_valor_pago;', (AmountRegister, PriceRegister, PriceRegister)) #INSERE NA TABELA estoque O ID DO PRODUTO E A QUANTIDADE ATUAL
        connection.commit() #INSERT INTO estoque (produto_id, qtd_atual, valor_venda) SELECT produto_id, qtd, 9.99 FROM itens_entrada
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

#if __name__ == "__main__":
#   StorageRegisterClassDB.CreateStorageDB()