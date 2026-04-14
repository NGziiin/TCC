import customtkinter as ctk
from customtkinter import CTkProgressBar, CTkFrame, CTkLabel
import customtkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os

class InterfaceLoading:
    def __init__(self, janela):
        self.janela = janela
        self.configAll()
        self.PositionWindow()
        self.ElementsInterface()
        self.close_app()

    def PositionWindow(self):
        self.janela.update_idletasks()
        self.largura = 600
        self.altura = 400
        self.height = self.janela.winfo_screenheight() #Altura
        self.width = self.janela.winfo_screenwidth() #Largura
        self.y = (self.height // 2) - (self.altura // 2)
        self.x = (self.width // 2) - (self.largura // 2)
        self.janela.geometry(f'{self.largura}x{self.altura}+{self.x}+{self.y}')

    def configAll(self):
        self.janela.resizable(False ,False)
        self.janela.overrideredirect(True)
        self.janela.attributes("-topmost",True)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        #VARIÁVEL COM O TEXTO QUE APARECE
        self.NameLoading = tk.StringVar(value="Olá")


    def ElementsInterface(self):

        # configuração do gif
        self.background = os.path.join(self.base_dir, 'image', 'background_loading.gif' or '*.gif') #diretório para o Gif
        self.frames = []
        self.gif = Image.open(self.background)

        self.resolutionGif = (self.largura, self.altura)

        for frame in ImageSequence.Iterator(self.gif):
            frameResized = frame.convert("RGBA").resize(self.resolutionGif, Image.Resampling.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(frameResized))

        self.idx = 0

        # fim da configuração do gif

        self.frameBackground = CTkFrame(self.janela)
        self.frameBackground.pack(anchor='center', fill='both', expand=True)

        #jogar o background da pasta imagens para aqui
        self.Background = CTkLabel(self.frameBackground, image=self.frames[0], text='')
        self.Background.pack(anchor='center', fill='both', expand=True)

        self.animateGif()

        #BARRA DE LOADING
        self.progressbar = CTkProgressBar(self.frameBackground,
                                          orientation='horizontal',
                                          width=250,
                                          height=12,
                                          corner_radius=6,
                                          border_width=1,
                                          fg_color='#2E2E2E',
                                          progress_color='#64BD15',
                                          mode='determinate')
        self.progressbar.place(relx=0.25, rely=0.65, anchor='center')
        self.progressbar.lift()
        self.textInfoLoading = CTkLabel(self.frameBackground, text_color="BLACK",
                                        textvariable=self.NameLoading,
                                        bg_color='transparent',
                                        font=('Segoe UI', 18))
        self.textInfoLoading.place(relx=0.25, rely=0.6, anchor='center')



    def animateGif(self): #CRIA A ANIMAÇÃO DENTRO DO GIF PARA LOADING
        self.idx = (self.idx + 1) % len(self.frames)
        self.Background.configure(image=self.frames[self.idx])
        self.janela.after(48, self.animateGif)

    def close_app(self, contador=0, contagembar=0.00): #DELETAR DEPOIS
        if contador < 50:
            match contador:
                case 0:
                    self.NameLoading.set('Olá')
                case 20:
                    self.NameLoading.set("tudo bem?")
                case 30:
                    self.NameLoading.set("sim! eu estou crescendo")
                case 40:
                    self.NameLoading.set("esse é o inicio da minha\nevolução")
                    self.textInfoLoading.place(rely=0.57)

            self.progressbar.set(contagembar)
            self.janela.after(500, lambda: self.close_app(contador + 1, contagembar + 0.02))
            print(f"{contador}\ncontagembar: {contagembar}")
        else:
            self.progressbar.set(1.0)
            self.janela.destroy()

if __name__ == "__main__":
    janela = ctk.CTk()
    InterfaceLoading(janela)
    janela.mainloop()
