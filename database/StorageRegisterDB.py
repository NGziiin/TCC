import sqlite3 as sqlite3
from tkinter import ttk
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

    def LoadStorageDB(listbox):
        connection = sqlite3.connect(StorageDbPath)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM storage')
        infos = cursor.fetchall()
        connection.commit()
        cursor.close()
        for linhas in infos:
            id_, cod, produto, quantidade, preco = linhas
            listbox.insert('', 'end', text=f'{cod}', values=(produto, quantidade, f'R$ {preco:,.2f}'.replace('.', ',')))

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