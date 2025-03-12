from tkinter import *
import sys
import os

def close_app():
    janela.quit()
    janela.destroy()

def frame_clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def informações():
    gui_base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(gui_base, 'gui'))
    from gui import principal
    principal.janelainicial(frameinfo)

def botoes():

    def on_enter(e):
        e.widget.config(bg='#fafafa')
    
    def on_leave(e):
        e.widget.config(bg='white')

    texto_botões = ['Vendas', 'Estoque', 'Registro de produtos', 'Clientes']

    frame_botões = Frame(framebutton, bg=framebutton.cget('bg'))
    frame_botões.pack(expand=True, fill=X)

    for texto in texto_botões:
        btn = Button(frame_botões, text=texto, font=('arial', 16), border=0, bg='white')
        btn.pack(pady=10, fill=X)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    

janela = Tk()

janela.geometry('1920x1040')
janela.state('zoomed')
janela.configure(bg='blue')

framebutton = Frame(janela, bg='white')
framebutton.place(relheight=0.99, relwidth=0.15, relx=0.002, rely=0.005)

frameinfo = Frame(janela, bg='white')
frameinfo.place(relheight=0.99, relwidth=0.842, relx=0.155, rely=0.005)

botoes()
informações()

janela.protocol("WM_DELETE_WINDOW", close_app)
janela.mainloop()