from tkinter import *
import sys
import os

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
    from gui.principal import janelainicial
    from gui.vendas import janela_vendas

def janela_inicial(frameinfo, frame):
    frame_clear(frame)
    imports()
    janelainicial(frameinfo)

def abrir_vendas(frame):
    frame_clear(frame)
    imports()
    janela_vendas(frameinfo)

def abrir_estoque():
    return

def abrir_registro():
    return

def abrir_clientes():
    return

def botoes(framebutton, frameinfo):

    def on_enter(e):
        e.widget.config(bg='#fafafa')
    
    def on_leave(e):
        e.widget.config(bg='white')

    texto_botões = {'Principal' : janela_inicial,
                    'Vendas' : abrir_vendas, 
                    'Estoque' : abrir_estoque, 
                    'Registro de produtos':abrir_registro, 
                    'Clientes': abrir_clientes}

    frame_botões = Frame(framebutton, bg=framebutton.cget('bg'))
    frame_botões.pack(expand=True, fill=X)

    for texto, funcao in texto_botões.items():
        btn = Button(frame_botões, text=texto, font=('arial', 16), border=0, bg='white', command=lambda f=frameinfo, func=funcao: func(f))
        btn.pack(pady=10, fill=X)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
#inicio do software
janela = Tk()

janela.geometry('1920x1040')
janela.state('zoomed')
janela.configure(bg='blue')

framebutton = Frame(janela, bg='white')
framebutton.place(relheight=0.99, relwidth=0.15, relx=0.002, rely=0.005)

frameinfo = Frame(janela, bg='white')
frameinfo.place(relheight=0.99, relwidth=0.842, relx=0.155, rely=0.005)

botoes(framebutton, frameinfo)
janela_inicial(frameinfo, frame)

janela.protocol("WM_DELETE_WINDOW", close_app)
janela.mainloop()