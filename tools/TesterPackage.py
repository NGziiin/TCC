import subprocess

class PackageTest:
    def __init__(self):
        ConectionInfo = self.ConectionTest()
        print(ConectionInfo)

    def ConectionTest(self):
        self.resultado = subprocess.run("ping www.google.com", capture_output=True, text=True)

        if self.resultado.returncode != 0:
            #BANCO DE DADOS LOCAL - SQLITE
            #CASO ESTEJA SEM INTERNET IRÁ RETORNAR FALSE
            print(f"sistema offline, iniciando banco de dados local")
            return False
        else:
            #BANCO DE DADOS ONLINE - POSTGRE
            #CASO POSSUA INTERNET RETORNA TRUE
            print(f"sistema online, conectando no banco de dados online")
            return True

if "__main__" == __name__:
    conection = PackageTest()