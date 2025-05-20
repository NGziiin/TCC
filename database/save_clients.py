import sqlite3
import time
import os

def load_tabela(db_file):

    print('iniciando o load de tabela')

    if os.path.exists(db_file):
        print('arquivo existe')
        conn = sqlite3.connect('clientes.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients")
        print(cur.fetchall())
        conn.close()
        print('finalizando o load de tabela')

    else:
        print('arquivo não existe')
        time.sleep(2)
        print("iniciando a criação de tabela")
        criando_tabela(db_file)


def criando_tabela(db_file):

    print('iniciando a criação de tabela')

    if os.path.exists(db_file):
        print('tabela existe')
        time.sleep(2)
        load_tabela(db_file)

    else:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS clients('
                    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'fname TEXT,'
                    'sname TEXT,'
                    'state TEXT,'
                    'city TEXT,'
                    'cpf REAL)') #fname = first name (primeiro nome) && sname = second name (segundo nome) && state = estado
        cur.fetchall()
        conn.close()
        print('finalizando a criação de tabela')
        time.sleep(2)
        print("iniciando o salvar tabela")
        salvando_tabela(db_file)

def salvando_tabela(db_file):
    print("iniciado o salvar tabela")
    teste = {
        'fname' : 'herick',
        'sname' : 'alves',
        'state' : 'goiás',
        'city' : 'campos belos',
        'cpf' : 71325245186
    }

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    print(teste)
    cur.execute('UPDATE clients SET fname = ?, sname = ?, state = ?, city = ?, cpf = ?'
                , (teste['fname'], teste['sname'], teste['state'], teste['city'], teste['cpf']))
    conn.commit()
    conn.close()
    print('finalizando as informações salvas')
    time.sleep(2)
    load_tabela(db_file)

print('iniciando o teste')
db_file = "../database/clientes.db"
if os.path.exists(db_file):
    print('existe o arquivo')
    time.sleep(15)
    load_tabela(db_file)
else:
    print('não existe no arquivo')
    time.sleep(15)
    criando_tabela(db_file)