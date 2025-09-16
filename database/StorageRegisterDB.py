import sqlite3 as sqlite3
import os, random

Storage_DB = 'StorageDb.db'
StorageDbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), Storage_DB)

class StorageRegisterDB:
    def __init__(self):
        self.connection = sqlite3.connect(StorageDbPath)
        self.cursor = self.connection.cursor()
        self.create_table()

    def CreateStorageDB(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage (
                id INTEGER PRIMARY KEY,
                item_cod INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                item_quantidade INTEGER NOT NULL,
                item_price INTEGER NOT NULL
            )
        ''')
        self.connection.commit()
        self.connection.close()

    def AddStorageDB(self):
        connection = sqlite3.connect(StorageDbPath)
        cursor = connection.cursor()
        codigo = [random.randint(0, 5000) for _ in range(7)]
        produto = ['Maçã', 'Pêra', 'Uva', 'Goiaba', 'Café', 'Sushi', 'Almôndegas']
        quantidade = [random.randint(0, 30) for _ in range(7)]
        preco = [random.randint(0, 200) for _ in range(7)]
        # Juntando tudo em uma lista de produto
        itens = []
        for i in range(7):
            item = {
                'Código': codigo[i],
                'Produto': produto[i],
                'Quantidade': quantidade[i],
                'Preço': preco[i]
                }
            itens.append(item)
        # Exibindo os dados
        for item in itens:
            print(item)
            cursor.execute('INSERT INTO storage (item_cod, item_name, item_quantidade, item_price) VALUES (?, ?, ?, ?)',
                            (item['Código'], item['Produto'], item['Quantidade'], item['Preço']))
        connection.commit()
        cursor.close()


#StorageRegisterDB()
StorageRegisterDB.AddStorageDB(self=True)