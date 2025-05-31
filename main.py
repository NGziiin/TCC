from tkinter import *
import sys
import os

from gui.registro_produto import janela_registro_produto


def close_app():
    janela.quit()
    janela.destroy()

def frame_clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def imports():
    gui_base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(gui_base, 'gui'))
    global janelainicial
    global janela_vendas
    global janela_estoque
    global janela_registro_produto
    global aba_relatorios
    from gui.principal import janelainicial
    from gui.vendas import janela_vendas
    from gui.estoque import janela_estoque
    from gui.registro_produto import janela_registro_produto
    from gui.relatorios import aba_relatorios

def janela_inicial(frameinfo):
    frame_clear(frameinfo)
    imports()
    janelainicial(frameinfo)

def abrir_vendas(frameinfo):
    frame_clear(frameinfo)
    imports()
    janela_vendas(frameinfo)

def abrir_estoque(frameinfo):
    frame_clear(frameinfo)
    imports()
    janela_estoque(frameinfo)

def janela_relatorio(frameinfo):
    frame_clear(frameinfo)
    imports()
    aba_relatorios(frameinfo)

def botoes(framebutton, frameinfo):

    def on_enter(e):
        e.widget.config(bg='#fafafa', fg='black')
    
    def on_leave(e):
        e.widget.config(bg='#E5E7EB', fg='black')

    texto_botões = {'Principal' : janela_inicial,
                    'Vendas' : abrir_vendas, 
                    'Estoque' : abrir_estoque,
                    'Relatório': janela_relatorio}

    frame_botões = Frame(framebutton, bg=framebutton.cget('bg'))
    frame_botões.pack(expand=True, fill=X)

    for texto, funcao in texto_botões.items():
        btn = Button(frame_botões, text=texto, font=('arial', 16), border=0, bg='#E5E7EB', fg='black', command=lambda f=frameinfo, func=funcao: func(f))
        btn.pack(pady=10, fill=X)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    

#inicio do software
janela = Tk()

janela.geometry('1920x1040')
janela.state('zoomed')
janela.configure(bg='#F97316')
janela.title("sistema de estoque - Lojas TCC & LTDA")

framebutton = Frame(janela, bg=janela.cget('bg'))
framebutton.place(relheight=0.99, relwidth=0.15, relx=0.002, rely=0.005)

frameinfo = Frame(janela, bg=janela.cget('bg'))
frameinfo.place(relheight=0.99, relwidth=0.842, relx=0.155, rely=0.005)

botoes(framebutton, frameinfo)
janela_inicial(frameinfo)

janela.protocol("WM_DELETE_WINDOW", close_app)
janela.mainloop()