import subprocess
from dotenv import load_dotenv
import pyodbc, os, json, time, threading, messagebox
load_dotenv()

#CLASSE COM FUNÇÕES INTERNAS
class InternalFunctions:

    @classmethod
    def count(cls, package_instance):
        print(f'{'-'*50}\niniciando contagem\nvariável da contagem em: {package_instance.contagem}\n{"-"*50}')
        for i in range(package_instance.contagem,5001):
            package_instance.contagem = i / 100
            print(f'{package_instance.contagem} - variável infocount: {package_instance.StopStart_Count}')
            time.sleep(1)
            if package_instance.contagem == 1:
                print('parando')
                break
            elif package_instance.StopStart_Count == True:
                print('parando')
                package_instance.contagem = int(package_instance.contagem * 100)
                print(package_instance.contagem)
                print('fim')
                break

class PackageTest:
    def __init__(self, TextLoading, progressbar):

        #DECLARAÇÃO DAS VARIÁVEIS
        self.resultado = None #variável usada para retorno de informações (ela retorna em forma sincrona evitando erros)
        self.TextLoading = TextLoading #OS TEXTOS DA TELA DE LOADING
        self.progressbar = progressbar #BARRA DE PROGRESSO PARA FAZER O LOADING
        self.contagem = int(0) #precisa iniciar em 0 - Variável que faz a contagem do loading
        self.StopStart_Count = False #variável para saber o momento de parar a contagem

        #inicinado os testes
        ConectionInfo = self.ConectionTest() #TESTE DE CONEXÃO DE REDE
        self.TestDB(ConectionInfo) #TESTE DO BANCO DE DADOS

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
            print(f"sistema offline, iniciando banco de dados local")
            self.StopStart_Count = True
            threadContagem.join()
            return False
        else:
            #BANCO DE DADOS ONLINE - AzureDB
            #CASO POSSUA INTERNET RETORNA TRUE
            print(f"sistema online, conectando no banco de dados online")
            self.StopStart_Count = True
            threadContagem.join()
            return True

    def TestDB(self, ConectionInfo):

        #ELE CRIA UM JSON COM TODAS AS INFORMAÇÕES DE TESTE PARA CASO PRECISE DENTRO DO SISTEMA
        def JSONConfig(ConectionInfo):
            self.baseDir = os.path.dirname(os.path.abspath(__file__))
            self.ReturnDir = os.path.dirname(self.baseDir)
            self.JSONFile = os.path.join(self.ReturnDir, 'configs', "tester.json")
            print(ConectionInfo)
            dadosNetwork = {
                "Network" : ConectionInfo
            }

            with open(self.JSONFile, "w", encoding="utf-8") as f:
                json.dump(dadosNetwork, f, indent=4)

            return

        #contagem da barra
        threadCount = threading.Thread(target=InternalFunctions.count,
                                       args=(self,),
                                       daemon=True)
        threadCount.start()
        time.sleep(1)

        self.ConectionInfo = ConectionInfo
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.retorno_dir = os.path.dirname(self.base_dir)
        self.msi_path = os.path.join(self.retorno_dir, "dependencies", 'msodbcsql.msi')

        #VERIFICAR AQUI PORQUE O CONTADOR PAROU DURANTE A EXECUÇÃO


        try:
            if self.ConectionInfo is True:  # se der retorno true é porque possui internet, com isso carrega o AzureDB
                print('verificando os drivers do AZURE SQL')
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
                            messagebox.showerror(title='Erro na instalação', message=f"Falha na instalação. Código: \n{install.returncode}\n"
                                                                                     f"Saida: {install.stdout}")
                            return

                    else:
                        print("driver já instalado")
                        pass

                except Exception as e:
                    print(f"Erro: {e}")
                    messagebox.showerror(title='Erro!',
                                         message=f"erro nos arquivos: {e}")
                    return

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
                    JSONConfig(self.ConectionInfo)
                    return

                except pyodbc.Error as e:
                    print(f"Erro: {e}")
                    JSONConfig(self.ConectionInfo)

            elif self.ConectionInfo is False:
                JSONConfig(self.ConectionInfo)

        except Exception as e:
            print(f"Erro: {e}")
            messagebox.showerror(title='Erro na conexão',
                                 message=f"erro para comunicar com o banco de dados: \n{e}")
            return

if __name__ == "__main__":
    teste = PackageTest(TextLoading=0, progressbar=0.00)