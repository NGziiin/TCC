from tkinter import *
from functools import *
import sys
import os

def imports():
   services = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
   sys.path.append(os.path.join(services, 'services'))
   global add_list
   from services.add_clients import add_list

def window_register():
   
   janela = Toplevel()

   imports()

   janela.geometry('400x400')
   janela.title('registrar cliente')

   btn = Button(janela, text='teste', font=('arial', 16), bg='white', fg='black', border=0, command=partial(add_list, frameclients))
   btn.pack(pady=10, fill=X)

   janela.mainloop()