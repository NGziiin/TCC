import sqlite3 as sqlite3
from tkinter import ttk
import os, messagebox

Storage_DB = 'StorageDb.db'
LowLimit_DB = 'LowLimitDb.db'
StorageDbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), Storage_DB)
LowLimitDbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), LowLimit_DB)

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

class StorageLowLimitDB:
    def __init__(self):
        pass

    def CreateLowLimitDB():
        connection = sqlite3.connect(LowLimitDbPath)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lowlimit (
                id INTEGER PRIMARY KEY,
                quantity_limit INTEGER NOT NULL
            )
        ''')
        connection.commit()
        connection.close()