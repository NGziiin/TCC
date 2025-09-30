import sqlite3 as sqlite3
import psycopg2
from tkinter import ttk
import os, messagebox

#Storage_DB = 'StorageDb.db'
#StorageDbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), Storage_DB)

class StorageRegisterClassDB:
    def __init__(self):
        pass

    def CreateStorageDB():
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage (
                id SERIAL PRIMARY KEY,
                item_cod INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                item_quantidade INTEGER NOT NULL,
                item_price INTEGER NOT NULL
            )
        ''')
        connection.commit()
        connection.close()

    def LoadStorageDB(listbox):
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
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
        connection = psycopg2.connect(host="localhost", port='5500', database="postgres", user="postgres", password="2004")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO storage (item_cod, item_name, item_quantidade, item_price) VALUES (%s, %s, %s, %s)',
                       (CodRegister, NameRegister, AmountRegister, PriceRegister))
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