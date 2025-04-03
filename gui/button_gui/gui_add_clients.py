from tkinter import *
from functools import *
import sys
import os

def imports():
   services = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
   sys.path.append(os.path.join(services, 'services'))
   global add_list
   from services.add_clients import add_list

def window_register(frame_nome, frame_sobrenome):
   
   janela = Toplevel()

   imports()

   #configurações da janela
   janela.geometry('400x400')
   janela.title('registrar cliente')

   #entrys das informações
   entry_name = Entry(janela, font=('arial', 16), bg='white', fg='black')
   entry_name.pack(pady=10, fill=X)

   entry_secname = Entry(janela, font=('arial', 16), bg='white', fg='black')
   entry_secname.pack(pady=2, fill=X)

   btn = Button(janela, text='teste', font=('arial', 16), bg='white', fg='black', border=0, command=partial(add_list, janela, frame_nome, entry_name, entry_secname, frame_sobrenome))
   btn.pack(pady=10, fill=X)

   janela.mainloop()