#AQUI É ONDE FICA O LOADING EM TEMPO REAL DO SOFTWARE
import time
import psycopg2.errors
from database.SoftwareDB import DBLog
from services.AnimationLoading import Start

class ClockUpdate:
    def __init__(self, frameAnimation):
        self.frameAnimation = frameAnimation
        self.logic()

    def logic(self):
        self.contador = 0
        while True:
            while self.contador < 20:
                time.sleep(0.5)
                self.contador += 1
                if self.contador == 20:
                    try:
                        animacao = Start(self.frameAnimation)
                        self.frameAnimation.after(2000, lambda: animacao.StopAnimation())
                        DBLog.LowStorage()
                        self.contador = 0
                    except psycopg2.errors.InvalidColumnReference:
                        self.contador = 0
                        pass