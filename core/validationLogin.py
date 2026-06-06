import pyodbc, os, jwt, hashlib
from dotenv import load_dotenv
import messagebox as msb

class ITFunctionLogin:

    @staticmethod
    def creatingHash(password: str) -> str:
        data = password.encode("utf-8")
        hash_object = hashlib.sha256(data)
        return hash_object.hexdigest()

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
        password = ITFunctionLogin.creatingHash(password) # cria a HASH para a senha
        AccountActive = True # variável para verificar se a conta está ativa
        Conn = ITFunctionLogin.GetUserDB()
        cursor = Conn.cursor()
        cursor.execute("SELECT UserID, Username FROM LoginAcess.AcessSystem WHERE "
                       "Username = ? "
                       "AND Password = ? "
                       "AND Status = ?;", (username, password, AccountActive ))
        result = cursor.fetchone()
        cursor.close()
        #CRIAR O RETORNO DE TOKEN PARA VALIDAÇÃO NO RESTO DA API
        if result is None:
            return {"Status" : False, "Token" : ''}
        else:
            tokenload = {
                "UserID" : result[0],
                "Username" : result[1],
            }
            Token_Acess = jwt.encode(tokenload,
                                     os.getenv('TK_PASSWORD'),
                                     algorithm='HS256')
            return {"Status" : True, "Token" : Token_Acess}