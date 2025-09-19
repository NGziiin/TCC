import sqlite3 as sqlite3
import os, messagebox

Storage_DB = 'StorageDb.db'
StorageDbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), Storage_DB)

class StorageRegisterClassDB:
    def __init__(self):
        pass

    def CreateStorageDB():
        connection = sqlite3.connect(StorageDbPath)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage (
                id INTEGER PRIMARY KEY,
                item_cod INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                item_quantidade INTEGER NOT NULL,
                item_price INTEGER NOT NULL
            )
        ''')
        connection.commit()
        connection.close()

    def AddStorageDB(CodRegister, NameRegister, AmountRegister, PriceRegister, janela):
        CodRegister = int(CodRegister.get())
        NameRegister = NameRegister.get()
        AmountRegister = int(AmountRegister.get())
        PriceRegister = float(PriceRegister.get().replace(',', '.'))
        connection = sqlite3.connect(StorageDbPath)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO storage (item_cod, item_name, item_quantidade, item_price) VALUES (?, ?, ?, ?)',
                       (CodRegister, NameRegister, AmountRegister, PriceRegister))
        connection.commit()
        cursor.close()
        janela.destroy()
        messagebox.showinfo('SUCESSO', 'Produto registrado com sucesso')

    def LoadStorageDB():
        connection = sqlite3.connect(StorageDbPath)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM storage')
        infos = cursor.fetchone()
        connection.commit()
        cursor.close()

        #passando só a primeira linha
        print(infos)
        id_, cod, produto, quantidade, preco = infos
        print(f'ID: {type(id_)}, CÓDIGO: {type(cod)}, PRODUTO: {type(produto)}, QUANTIDADE: {type(quantidade)}, PREÇO: {type(preco)}')
        print(id_, cod, produto, quantidade, preco)
