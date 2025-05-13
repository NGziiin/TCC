import sqlite3
import time
import os

def load_tabela():

    print('iniciando o load de tabela')

    conn = sqlite3.connect('clientes.db')
    cur = conn.cursor()
    info = cur.execute("SELECT fname, sname, state, city, cpf FROM clients")
    resultado = info.fetchone()
    print(resultado)

    print('finalizando o load de tabela')

def criando_tabela(db_file):

    print('iniciando a criação de tabela')

    teste = [
        'herick',
        'alves',
        'goiás',
        'campos belos',
        71325245186
    ]

    if os.path.exists(db_file):
        print('tabela existe')
        time.sleep(5)
        load_tabela()

    else:
        conn = sqlite3.connect('clientes.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE clients(fname, sname, state, city, cpf)') #fname = first name (primeiro nome) && sname = second name (segundo nome) && state = estado
        cur.execute("""
        INSERT INTO clients VALUES
        (?, ?, ?, ?, ?) 
        """, teste)
        cur.fetchall()

        print('finalizando a criação de tabela')

print('iniciando o teste')
db_file = "../database/clientes.db"
if os.path.exists(db_file):
    print('existe o arquivo')
    time.sleep(15)
    load_tabela()
else:
    print('não existe no arquivo')
    time.sleep(15)
    criando_tabela(db_file)