#AQUI É ONDE FICA O LOADING EM TEMPO REAL DO SOFTWARE
import time

import psycopg2.errors

from database.SoftwareDB import DBLog

class ClockUpdate:
    def __init__(self):
        self.logic()

    def logic(self):
        self.contador = 0
        while True:
            while self.contador < 50:
                time.sleep(0.5)
                self.contador += 1
                print(self.contador)
                if self.contador == 50:
                    try:
                        DBLog.LowStorage()
                        self.contador = 0
                        print('contador resetado')
                    except psycopg2.errors.InvalidColumnReference:
                        self.contador = 0
                        print('contador resetado')
                        pass

if __name__ == '__main__':
    ClockUpdate()