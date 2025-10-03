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
                       id SERIAL PRIMARY KEY,
                       produto INT NOT NULL,
                       qtd_atual INT NOT NULL,
                       valor_venda NUMERIC(10,2),
                       ultimo_valor_pago NUMERIC(10,2),
                       CONSTRAINT fk_produto FOREIGN KEY(produto) REFERENCES produto(id)
                       )''')
        
        #TABELA DE ENTRADA DE PRODUTO
        cursor.execute('''CREATE TABLE IF NOT EXISTS entrada_produto (
                       id SERIAL PRIMARY KEY,
                       data DATE NOT NULL,
                       descricao TEXT
                       )''')
        
        #TABELA DE ITENS DE ENTRADA
        cursor.execute('''CREATE TABLE IF NOT EXISTS itens_entrada (
                       id SERIAL PRIMARY KEY,
                       id_entrada INT NOT NULL,
                       produto INT NOT NULL,
                       qtd INT NOT NULL,
                       valor_unitario NUMERIC(10,2),
                       CONSTRAINT fk_entrada FOREIGN KEY (id_entrada) REFERENCES entrada_produto(id),
                       CONSTRAINT fk_produto_entrada FOREIGN KEY (produto) REFERENCES produto(id)
                       )''')
        
        #TABELA DE VENDA
        cursor.execute('''CREATE TABLE IF NOT EXISTS venda (
                       id SERIAL PRIMARY KEY,
                       data DATE NOT NULL,
                       total_venda NUMERIC(10,2)
                       )''')
        
        #TABELA DE ITENS VENDA
        cursor.execute('''CREATE TABLE IF NOT EXISTS itens_venda (
                       id SERIAL PRIMARY KEY,
                       id_venda INT NOT NULL,
                       produto INT NOT NULL,
                       qtd INT NOT NULL,
                       valor_unitario NUMERIC(10,2),
                       CONSTRAINT fk_venda FOREIGN KEY (id_venda) REFERENCES venda(id),
                       CONSTRAINT fk_produto_venda FOREIGN KEY (produto) REFERENCES produto(id)
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

    def AddStorageDB(CodRegister, NameRegister, AmountRegister, PriceRegister, DescriçaoRegister, janela):
        Dateregister = datetime.date.today()
        Dateregister = Dateregister.strftime('%d-%m-%Y') #SALVA A DATA NO NA TABELA entrada_produto NA COLUNA descrição
        CodRegister = int(CodRegister.get())
        NameRegister = NameRegister.get()
        DescriçaoRegister = DescriçaoRegister.get()
        AmountRegister = int(AmountRegister.get())
        PriceRegister = float(PriceRegister.get().replace(',', '.'))
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO entrada_produto (data, descricao) VALUES (%s, %s);', (Dateregister, DescriçaoRegister))
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

if __name__ == "__main__":
    #StorageRegisterClassDB.AddStorageDB(CodRegister=True, NameRegister=True, AmountRegister=True, PriceRegister=True, DescriçaoRegister=True, janela=True)
    StorageRegisterClassDB.CreateStorageDB()