import subprocess, socket
from dotenv import load_dotenv
import pyodbc, os, json, time, threading, messagebox, uvicorn
from fastapi import FastAPI

load_dotenv()
server = FastAPI()

#CLASSE COM FUNÇÕES INTERNAS
class InternalFunctions:

    @classmethod
    def count(cls, package_instance):
        print(f'{'-'*50}\n'
              f'[DEBUG] iniciando contagem'
              f'\n[DEBUG] variável da contagem em: {package_instance.contagem}'
              f'\n{"-"*50}')

        for i in range(package_instance.contagem,101):

            package_instance.contagem = i / 100
            print(f'[DEBUG] {package_instance.contagem} - variável contagem: {package_instance.StopStart_Count}')
            package_instance.progressbar.after(0, lambda v=package_instance.contagem: package_instance.progressbar.set(v))
            
            time.sleep(1)
            if package_instance.contagem == 1:
                print('[DEBUG] parando')
                break
            elif package_instance.StopStart_Count == True:
                print('[DEBUG] parando')
                package_instance.contagem = int(package_instance.contagem * 100)
                print(f"[DEBUG] valor do calculo: {package_instance.contagem}\n{"-"*30}")
                break

class PackageTest:
    def __init__(self, TextLoading, progressbar, janela):

        #DECLARAÇÃO DAS VARIÁVEIS
        self.resultado = None #variável usada para retorno de informações (ela retorna em forma sincrona evitando erros)
        self.TextLoading = TextLoading #OS TEXTOS DA TELA DE LOADING
        self.progressbar = progressbar #BARRA DE PROGRESSO PARA FAZER O LOADING
        self.contagem = int(0) #precisa iniciar em 0 - Variável que faz a contagem do loading
        self.StopStart_Count = False #variável para saber o momento de parar a contagem
        self.PathMain = os.path.dirname(os.path.abspath(__file__)) #pega a pasta main
        self.PathElectron = os.path.dirname(self.PathMain) #RETORNA UMA PASTA
        self.ElectronOpen = os.path.join(self.PathElectron, 'electron-app')  # inicia o arquivo index.js
        self.janela = janela

        self.InitTest() #Variável que inicia todos os testes


    def InitTest(self):
        # inicinado os testes
        self.TextLoading.set("Iniciando os testes")
        ConectionInfo = self.ConectionTest()  # TESTE DE CONEXÃO DE REDE
        self.contagem = int(50)
        self.TestDB(ConectionInfo)  # TESTE DO BANCO DE DADOS
        self.contagem = int(90)
        self.OpenServerLocal() #ABRE O SERVER LOCAL.
        self.OpenSoftware()

    def ConectionTest(self):

        threadContagem = threading.Thread(target=InternalFunctions.count,
                         args=(self,),
                         daemon=True)#contagem e atualização da barra de loading
        threadContagem.start()
        self.TextLoading.set('Iniciando teste de rede')
        self.resultado = subprocess.run("ping www.google.com", capture_output=True, text=True)

        if self.resultado.returncode != 0:
            #BANCO DE DADOS LOCAL - SQLITE
            #CASO ESTEJA SEM INTERNET IRÁ RETORNAR FALSE
            print(f"[DEBUG] sistema offline, iniciando banco de dados local")
            self.StopStart_Count = True
            threadContagem.join()
            self.TextLoading.set('teste de rede concluido')
            return False
        else:
            #BANCO DE DADOS ONLINE - AzureDB
            #CASO POSSUA INTERNET RETORNA TRUE
            print(f"[DEBUG] sistema online, conectando no banco de dados online")
            self.StopStart_Count = True
            threadContagem.join()
            self.TextLoading.set('teste de rede concluido')
            return True

    def TestDB(self, ConectionInfo):

        #ELE CRIA UM JSON COM TODAS AS INFORMAÇÕES DE TESTE PARA CASO PRECISE DENTRO DO SISTEMA
        def JSONConfig(ConectionInfo):
            self.baseDir = os.path.dirname(os.path.abspath(__file__))
            self.ReturnDir = os.path.dirname(self.baseDir)
            self.JSONFile = os.path.join(self.ReturnDir, 'configs', "ConfigsSystem.json")
            print( f"[DEBUG] {ConectionInfo}")
            dadosNetwork = {
                "Network" : ConectionInfo
            }

            with open(self.JSONFile, "w", encoding="utf-8") as f:
                json.dump(dadosNetwork, f, indent=4)

            return

        def ConnectSystem():#por causa do sistema offline ele tenta conectar 2x
            print('[DEBUG] tentando conectar no banco de dados')
            connectiondb = pyodbc.connect(
                f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
                f"SERVER={os.getenv('DB_SERVER')};"
                f"DATABASE={os.getenv('DB_DATABASE')};"
                f"UID={os.getenv('DB_UID')};"
                f"PWD={os.getenv('DB_PWD')};"
                "Encrypt=yes;"
                "TrustServerCertificate=no;"
                "Connection Timeout=30;"
            )
            return connectiondb

        #contagem da barra
        self.StopStart_Count = False
        threadCount = threading.Thread(target=InternalFunctions.count,
                                       args=(self,),
                                       daemon=True)
        threadCount.start()
        self.TextLoading.set("iniciando testes no banco de dados")
        time.sleep(1)

        self.ConectionInfo = ConectionInfo
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.retorno_dir = os.path.dirname(self.base_dir)
        self.msi_path = os.path.join(self.retorno_dir, "dependencies", 'msodbcsql.msi')

        try:
            if self.ConectionInfo is True:  # se der retorno true é porque possui internet, com isso carrega o AzureDB
                time.sleep(1)
                self.TextLoading.set('Verificando driver do banco de dados')
                print('[DEBUG] verificando os drivers do AZURE SQL')
                driverAzure = pyodbc.drivers()

                #INSTALA O DRIVER PARA CONECTAR NO AZURE CASO NÃO ENCONTRE NA LISTA DE DRIVERS
                try:
                    if "ODBC Driver 18 for SQL Server" not in driverAzure:
                        print('[DEBUG] driver não instalado')
                        print("[DEBUG] iniciando instalação do driver")
                        self.StopStart_Count = True
                        threadCount.join()
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

                        self.TextLoading.set("instalando driver")
                        if install == 0:
                            self.StopStart_Count = False
                            threadCount.start()
                            print("[DEBUG] Instalação finalizada")
                            self.TextLoading.set('Driver instalado')
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
                    self.TextLoading.set('conectando no banco de dados')
                    try:
                        print("[DEBUG] primeira tentativa de conectar")
                        conn1 = ConnectSystem()
                        cursor1 = conn1.cursor()
                        cursor1.execute("select 1;")
                        print('[DEBUG] Primeira tentativa ok')
                    except pyodbc.Error as e:
                        print('[DEBUG] primeira tentativa deu erro: ',e)
                        self.StopStart_Count = True
                        threadCount.join()
                        time.sleep(60)
                        self.StopStart_Count = False
                        threadCount = threading.Thread(target=InternalFunctions.count,
                                                       args=(self,),
                                                       daemon=True)
                        threadCount.start()
                        #tenta conectar novamente caso dê erro
                        try:
                            print("[DEBUG] segunda tentativa de conectar")
                            conn2 = ConnectSystem()
                            cursor2 = conn2.cursor()
                            cursor2.execute("select 1;")
                            print('[DEBUG] Segunda tentativa ok')
                        except pyodbc.Error as e:
                            print('[DEBUG] segunda tentativa deu erro: ',e)
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
                    self.TextLoading.set('erro ao conectar no banco de dados')

            elif self.ConectionInfo is False:
                JSONConfig(self.ConectionInfo)
                self.StopStart_Count = True
                threadCount.join()
                self.TextLoading.set('carregando banco offline')

        except Exception as e:
            print(f"[DEBUG] Erro: {e}")
            messagebox.showerror(title='Erro interno',
                                 message=f"ocorreu um erro durante a verificação \n{e}")
            self.StopStart_Count = True
            threadCount.join()
            return

    def OpenServerLocal(self):
        try:
            self.StopStart_Count = False
            threadCount = threading.Thread(target=InternalFunctions.count,
                                           args=(self,),
                                           daemon=True)
            threadCount.start()
            self.TextLoading.set('Iniciando server local')

            #cria a porta automática
            sock = socket.socket()
            sock.bind(("127.0.0.1", 0))
            porta = sock.getsockname()[1]
            sock.close()
            print(porta)

            # Função para abrir o server
            self.config = uvicorn.Config("tools.APILocal:app", host='127.0.0.1', port=porta, reload=False)
            self.server = uvicorn.Server(self.config)
            def start_server():
                print('abrindo server')
                self.server.run()

            #abrindo o server
            self.resultado = threading.Thread(target=start_server, daemon=True)
            self.resultado.start()

            #anotando o ip no JSON
            self.baseDir = os.path.dirname(os.path.abspath(__file__))
            self.ReturnDir = os.path.dirname(self.baseDir)
            self.JSONFile = os.path.join(self.ReturnDir, 'configs', "ConfigsSystem.json")

            self.TextLoading.set("salvando informações")
            #aqui verifica se já possui o arquivo json
            if os.path.exists(self.JSONFile):
                with open(self.JSONFile, "r", encoding="utf-8") as f:
                    dadosJSON = json.load(f)

            else:
                dadosJSON = {}

            #adiciona a informação do ip
            dadosJSON["ip"] = f'http://{self.config.host}:{porta}'

            #salva novamente
            with open(self.JSONFile, "w", encoding="utf-8") as f:
                json.dump(dadosJSON, f, indent=4)

            self.StopStart_Count = True
            threadCount.join()
        except Exception as e:
            import traceback
            print(f"[DEBUG] Erro: {e}")
            traceback.print_exc()

    def OpenSoftware(self):
        self.StopStart_Count = True
        subprocess.Popen(['npx.cmd', 'electron', '.'], cwd=self.ElectronOpen)
        self.progressbar.set(1.0)
        self.janela.destroy()