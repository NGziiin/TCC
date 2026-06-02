import pyodbc, os
from dotenv import load_dotenv
import messagebox as msb

class ITFunctionLogin:

    @staticmethod
    def GetUserDB():
        load_dotenv()
        try:
            connect = pyodbc.connect(
                f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
                f"SERVER={os.getenv('DB_SERVER')};"
                f"DATABASE={os.getenv('DB_DATABASE')};"
                f"UID={os.getenv('DB_UID')};"
                f"PWD={os.getenv('DB_PWD')};"
                "Encrypt=yes;"
                "TrustServerCertificate=no;"
                "Connection Timeout=30;"
            )
            return connect
        except pyodbc.Error as e:
            msb.showerror("Erro", "Erro ao verificar o acesso\n"
                                  "contate com o seu administrador")
            print(f"[DEBUG] Erro ao verificar o acesso: {e}")
            pass

    @staticmethod
    def login(username, password):
        AccountActive = True # variável para verificar se a conta está ativa
        Conn = ITFunctionLogin.GetUserDB()
        cursor = Conn.cursor()
        cursor.execute("SELECT 1 FROM LoginAcess.AcessSystem WHERE "
                       "Username = ? "
                       "AND Password = ? "
                       "AND Status = ?;", (username, password, AccountActive ))

        #CRIAR O RETORNO DE TOKEN PARA VALIDAÇÃO NO RESTO DA API
        if cursor.rowcount == 0:
            print('nenhum acesso encontrado')
            cursor.close()
            return False
        else:
            print('acesso encontrado')
            cursor.close()
            return True