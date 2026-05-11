import subprocess
from dotenv import load_dotenv
import pyodbc, os
load_dotenv()

class PackageTest:
    def __init__(self):
        self.resultado = None #variável usada para retorno de informações (ela retorna em forma sincrona evitando erros)
        ConectionInfo = self.ConectionTest()
        self.LoadDB(ConectionInfo)

    def ConectionTest(self):
        self.resultado = subprocess.run("ping www.google.com", capture_output=True, text=True)

        if self.resultado.returncode != 0:
            #BANCO DE DADOS LOCAL - SQLITE
            #CASO ESTEJA SEM INTERNET IRÁ RETORNAR FALSE
            print(f"sistema offline, iniciando banco de dados local")
            return False
        else:
            #BANCO DE DADOS ONLINE - AzureDB
            #CASO POSSUA INTERNET RETORNA TRUE
            print(f"sistema online, conectando no banco de dados online")
            return True

    def LoadDB(self, ConectionInfo):

        #VERIFICA O BANCO DE DADOS SQLITE3
        def verifiedSqlite3(self):
            print('verificando o SQLite')
            self.resultado = subprocess.run("sqlite3 --version", capture_output=True, text=True)
            print(self.resultado.returncode)
            return

        self.ConectionInfo = ConectionInfo
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.retorno_dir = os.path.dirname(self.base_dir)
        self.msi_path = os.path.join(self.retorno_dir, "dependencies", 'msodbcsql.msi')
        try:
            if self.ConectionInfo is True:  # se der retorno true é porque possui internet, com isso carrega o AzureDB
                print('verificando o acesso ao AZURE SQL')

                driverAzure = pyodbc.drivers()

                #INSTALA O DRIVER PARA CONECTAR NO AZURE CASO NÃO ENCONTRE NA LISTA DE DRIVERS
                try:
                    if "ODBC Driver 18 for SQL Server" not in driverAzure:
                        print('driver não instalado')
                        print("iniciando instalação do driver")
                        print(self.msi_path)
                        install = subprocess.run(['msiexec',
                                                  "/i",
                                                  self.msi_path,
                                                  "/norestart",
                                                  "IACCEPTMSODBCSQLLICENSETERMS=YES",
                                                  ],
                                                 capture_output=True,
                                                 text=True,
                                                 check=True
                                                 )

                        if install == 0:
                            print("Instalação finalizada")
                            pass

                        else:
                            print(f"falha na instalação. código: {install.returncode}")
                            print(f"Saida: {install.stdout}")
                            return

                    else:
                        print("driver já instalado")
                        pass

                except Exception as e:
                    print(f"Erro: {e}")
                    return

                try:
                    self.connectiondb = pyodbc.connect(
                        f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
                        f"SERVER={os.getenv('DB_SERVER')};"
                        f"DATABASE={os.getenv('DB_DATABASE')};"
                        f"UID={os.getenv('DB_UID')};"
                        f"PWD={os.getenv('DB_PWD')};"
                        "Encrypt=yes;"
                        "TrustServerCertificate=no;"
                        "Connection Timeout=30;"
                    )
                    cursor = self.connectiondb.cursor()
                    cursor.execute("SELECT 1;")
                    print('banco de dados: AZURE SQL')
                    return

                except pyodbc.Error as e:
                    print(f"Erro: {e}")
                    verifiedSqlite3(self)

            elif self.ConectionInfo is False:
                verifiedSqlite3(self)

        except Exception as e:
            print(f"Erro: {e}")
            return

if "__main__" == __name__:
    conection = PackageTest()