import subprocess
from dotenv import load_dotenv
import pyodbc, os, json, time, threading, messagebox
from flask import Flask


load_dotenv()
server = Flask(__name__)

#CLASSE COM FUNÇÕES INTERNAS
class InternalFunctions:

    @classmethod
    def count(cls, package_instance):
        print(f'{'-'*50}\n'
              f'[DEBUG] iniciando contagem'
              f'\n[DEBUG] variável da contagem em: {package_instance.contagem}'
              f'\n{"-"*50}')
        for i in range(package_instance.contagem,5001):
            package_instance.contagem = i / 100
            print(f'[DEBUG] {package_instance.contagem} - variável contagem: {package_instance.StopStart_Count}')
            time.sleep(1)
            if package_instance.contagem == 1:
                print('[DEBUG] parando')
                break
            elif package_instance.StopStart_Count == True:
                print('[DEBUG] parando')
                package_instance.contagem = int(package_instance.contagem * 100)
                print(f"[DEBUG] {package_instance.contagem}\n{"-"*30}")
                break

class PackageTest:
    def __init__(self, TextLoading, progressbar):

        #DECLARAÇÃO DAS VARIÁVEIS
        self.resultado = None #variável usada para retorno de informações (ela retorna em forma sincrona evitando erros)
        self.TextLoading = TextLoading #OS TEXTOS DA TELA DE LOADING
        self.progressbar = progressbar #BARRA DE PROGRESSO PARA FAZER O LOADING
        self.contagem = int(0) #precisa iniciar em 0 - Variável que faz a contagem do loading
        self.StopStart_Count = False #variável para saber o momento de parar a contagem

        self.InitTest() #Variável que inicia todos os testes


    def InitTest(self):
        # inicinado os testes
        ConectionInfo = self.ConectionTest()  # TESTE DE CONEXÃO DE REDE
        self.TestDB(ConectionInfo)  # TESTE DO BANCO DE DADOS
        self.OpenServerLocal() #ABRE O SERVER LOCAL.

    def ConectionTest(self):

        threadContagem = threading.Thread(target=InternalFunctions.count,
                         args=(self,),
                         daemon=True)#contagem e atualização da barra de loading
        threadContagem.start()
        #self.TextLoading.set('Iniciando teste de rede') <<- tirar o comentário
        self.resultado = subprocess.run("ping www.google.com", capture_output=True, text=True)

        if self.resultado.returncode != 0:
            #BANCO DE DADOS LOCAL - SQLITE
            #CASO ESTEJA SEM INTERNET IRÁ RETORNAR FALSE
            print(f"[DEBUG] sistema offline, iniciando banco de dados local")
            self.StopStart_Count = True
            threadContagem.join()
            return False
        else:
            #BANCO DE DADOS ONLINE - AzureDB
            #CASO POSSUA INTERNET RETORNA TRUE
            print(f"[DEBUG] sistema online, conectando no banco de dados online")
            self.StopStart_Count = True
            threadContagem.join()
            return True

    def TestDB(self, ConectionInfo):

        #ELE CRIA UM JSON COM TODAS AS INFORMAÇÕES DE TESTE PARA CASO PRECISE DENTRO DO SISTEMA
        def JSONConfig(ConectionInfo):
            self.baseDir = os.path.dirname(os.path.abspath(__file__))
            self.ReturnDir = os.path.dirname(self.baseDir)
            self.JSONFile = os.path.join(self.ReturnDir, 'configs', "tester.json")
            print( f"[DEBUG] {ConectionInfo}")
            dadosNetwork = {
                "Network" : ConectionInfo
            }

            with open(self.JSONFile, "w", encoding="utf-8") as f:
                json.dump(dadosNetwork, f, indent=4)

            return

        #contagem da barra
        self.StopStart_Count = False
        threadCount = threading.Thread(target=InternalFunctions.count,
                                       args=(self,),
                                       daemon=True)
        threadCount.start()
        time.sleep(1)

        self.ConectionInfo = ConectionInfo
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.retorno_dir = os.path.dirname(self.base_dir)
        self.msi_path = os.path.join(self.retorno_dir, "dependencies", 'msodbcsql.msi')

        try:
            if self.ConectionInfo is True:  # se der retorno true é porque possui internet, com isso carrega o AzureDB
                time.sleep(1)
                print('[DEBUG] verificando os drivers do AZURE SQL')
                driverAzure = pyodbc.drivers()

                #INSTALA O DRIVER PARA CONECTAR NO AZURE CASO NÃO ENCONTRE NA LISTA DE DRIVERS
                try:
                    if "ODBC Driver 18 for SQL Server" not in driverAzure:
                        print('[DEBUG] driver não instalado')
                        print("[DEBUG] iniciando instalação do driver")
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
                            print("[DEBUG] Instalação finalizada")
                            pass

                        else:
                            print(f"[DEBUG] falha na instalação. código: {install.returncode}")
                            print(f"[DEBUG] Saida: {install.stdout}")
                            messagebox.showerror(title='Erro na instalação',
                                                 message=f"Falha na instalação. Código: "
                                                         f"\n{install.returncode}\n"
                                                         f"Saida: {install.stdout}")
                            self.StopStart_Count = True
                            threadCount.join()
                            return

                    else:
                        print("[DEBUG] driver já instalado")
                        pass

                except Exception as e:
                    print(f"[DEBUG] Erro: {e}")
                    messagebox.showerror(title='Erro!',
                                         message=f"erro durante a instalação dos drivers: \n{e}")
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
                    print('[DEBUG] banco de dados: AZURE SQL')
                    JSONConfig(self.ConectionInfo)
                    self.StopStart_Count = True
                    threadCount.join()
                    return

                except pyodbc.Error as e:
                    print(f"[DEBUG] Erro: {e}")
                    self.ConectionInfo = False
                    JSONConfig(self.ConectionInfo)
                    self.StopStart_Count = True
                    threadCount.join()

            elif self.ConectionInfo is False:
                JSONConfig(self.ConectionInfo)
                self.StopStart_Count = True
                threadCount.join()

        except Exception as e:
            print(f"[DEBUG] Erro: {e}")
            messagebox.showerror(title='Erro interno',
                                 message=f"ocorreu um erro durante a verificação \n{e}")
            self.StopStart_Count = True
            threadCount.join()
            return

    def OpenServerLocal(self):
        server.run(debug=True, port=433, use_reloader=False)

if __name__ == "__main__":
    teste = PackageTest(TextLoading=0, progressbar=0)