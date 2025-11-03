####DELETAR ESSE ARQUIVO QUANDO FINALIZAR O DESENVOLVIMENTO DO SOFTWARE




import psycopg2
from faker import Faker
import random
from datetime import datetime

class AutoTeste:
    def __init__(self):
        self.PreencherDBAutomaticamente()

    def PreencherDBAutomaticamente(self):
        fake = Faker('pt_BR')  # Gera dados no estilo brasileiro

        # Conexão com o banco
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password="2004"
        )
        cursor = connection.cursor()

        # Gerar e inserir 10 produtos fictícios
        for _ in range(30):
            # Dados simulados
            NameRegister = fake.unique.word().capitalize()
            MarcaRegister = fake.company()
            AmountRegister = random.randint(1, 100)
            PriceRegister = round(random.uniform(5.0, 500.0), 2)
            Porcentagem = random.choice([10, 20, 30, 40])
            MargemRegister = f"{Porcentagem}%"
            lucro = PriceRegister * (Porcentagem / 100)
            ValorVenda = round(PriceRegister + lucro, 2)
            Dateregister = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            LogRegister = f'Foi registrado o produto {NameRegister}'
            LogProdutoRegister = f'Foi registrado o produto na data: {Dateregister}'

            # Verificar se já existe
            cursor.execute('SELECT id FROM produto WHERE nome = %s', (NameRegister,))
            verify_nome = cursor.fetchone()
            cursor.execute('SELECT id FROM produto WHERE marca = %s', (MarcaRegister,))
            verify_marca = cursor.fetchone()

            if verify_nome is None or verify_marca is None:
                # Inserir entrada_produto
                cursor.execute('INSERT INTO entrada_produto (data, descricao) VALUES (%s, %s) RETURNING id;',
                               (Dateregister, LogRegister))
                id_entrada = cursor.fetchone()[0]

                # Inserir produto
                cursor.execute(
                    'INSERT INTO produto (nome, descricao, marca, margem_lucro) VALUES (%s, %s, %s, %s) RETURNING id;',
                    (NameRegister, LogProdutoRegister, MarcaRegister, MargemRegister))
                id_produto = cursor.fetchone()[0]

                # Inserir itens_entrada
                cursor.execute(
                    'INSERT INTO itens_entrada (id_entrada, produto_id, qtd, valor_unitario) VALUES (%s, %s, %s, %s);',
                    (id_entrada, id_produto, AmountRegister, PriceRegister))

                # Inserir estoque
                cursor.execute(
                    'INSERT INTO estoque (produto_id, qtd_atual, valor_venda, ultimo_valor_pago) VALUES (%s, %s, %s, %s);',
                    (id_produto, AmountRegister, ValorVenda, PriceRegister))

                # Inserir log
                cursor.execute('INSERT INTO log (tipo, produto, marca, quantidade, data) VALUES (%s, %s, %s, %s, %s);',
                               ('Adicionado', NameRegister, MarcaRegister, AmountRegister, Dateregister))

                print(f"[✔] Produto '{NameRegister}' inserido com sucesso.")

        connection.commit()
        cursor.close()
        connection.close()