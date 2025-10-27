#AQUI É ONDE FICA O LOADING EM TEMPO REAL DO SOFTWARE

import time

class ClockUpdate:
    def __init__(self):
        self.logic()

    def logic(self):
        self.contador = 0
        while self.contador < 50:
            time.sleep(0.5)
            self.contador += 1
            print(self.contador)
            if self.contador == 50:
                print('contador resetado')
                self.contador = 0