from customtkinter import CTk

class Interface:
    def __init__(self):
        self.WindowConfigure()

    def WindowConfigure(self):
        self.janela = CTk()
        self.janela.geometry('500x200')
        self.janela.title('Selecione o produto')
        self.janela.mainloop()


if __name__ == '__main__':
    Interface()