import sqlite3 as sqlite3
import os, messagebox

Storage_DB = 'StorageDb.db'
StorageDbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), Storage_DB)

class StorageRegisterDB:
    def __init__(self):
        self.connection = sqlite3.connect(StorageDbPath)
        self.cursor = self.connection.cursor()
        self.CreateStorageDB()

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

    def AddStorageDB(CodRegister, NameRegister, AmountRegister, PriceRegister, janela):
        CodRegister = int(CodRegister.get())
        NameRegister = NameRegister.get()
        AmountRegister = int(AmountRegister.get())
        PriceRegister = int(PriceRegister.get())
        connection = sqlite3.connect(StorageDbPath)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO storage (item_cod, item_name, item_quantidade, item_price) VALUES (?, ?, ?, ?)',
                       (CodRegister, NameRegister, AmountRegister, PriceRegister))
        connection.commit()
        cursor.close()
        janela.destroy()
        messagebox.showinfo('SUCESSO', 'Produto adicionado com sucesso')