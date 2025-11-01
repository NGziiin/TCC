from tkinter import *
import customtkinter
from customtkinter import *
import sys, os, threading
from database.SoftwareDB import StorageRegisterClassDB, StorageLowLimitDB
from services import TimerUpdate

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
    global aba_relatorios
    from gui.principal import janelainicial
    from gui.vendas import janela_vendas
    from gui.estoque import janela_estoque
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

    texto_botões = {'PRINCIPAL' : janela_inicial,
                    'VENDAS' : abrir_vendas,
                    'ESTOQUE' : abrir_estoque,
                    'RELATÓRIO': janela_relatorio}

    frame_botões = Frame(framebutton, bg=framebutton.cget('bg'))
    frame_botões.pack(expand=True, fill=X)

    for texto, funcao in texto_botões.items():
        btn = customtkinter.CTkButton(frame_botões, text=texto, font=('arial', 18, 'bold'), height=50, text_color='black', hover_color='#FFF7ED',  fg_color='#F97316', command=lambda f=frameinfo, func=funcao: func(f))
        btn.pack(pady=10, fill=X)

#inicio do software
janela = CTk()

threading.Thread(target=StorageRegisterClassDB.CreateStorageDB, daemon=True).start()
threading.Thread(target=StorageLowLimitDB.CreateLowLimitDB, daemon=True).start()
threading.Thread(target=TimerUpdate.ClockUpdate, daemon=True).start()

janela.geometry('1920x1040')
janela.after(100, lambda: janela.wm_state('zoomed'))
janela.configure(bg="#F8FAFC")
janela.title("sistema de estoque - Lojas TCC & LTDA")

framebutton = Frame(janela, bg=janela.cget('bg'))
framebutton.place(relheight=0.99, relwidth=0.15, relx=0.002, rely=0.005)

frameinfo = Frame(janela, bg='white')
frameinfo.place(relheight=1, relwidth=0.848, relx=0.155, rely=0)

botoes(framebutton, frameinfo)
janela_inicial(frameinfo)


janela.protocol("WM_DELETE_WINDOW", close_app)
janela.mainloop()