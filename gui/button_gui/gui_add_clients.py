from tkinter import *
from functools import *
from tkinter.ttk import Combobox
from pyUFbr.baseuf import ufbr
import sys
import os

class Funcoes:

   def pegando_dados(self, select_cidade):

      selecao = select_estado.get()
      cidades = ufbr.list_cidades(sigla=selecao)
      
      select_cidade["state"] = "readonly"
      select_cidade["values"] = cidades
      select_cidade.set("Selecione a cidade")
      
   def biblioteca(self):
      
      global estado
      estado = (ufbr.list_uf)
      
   def imports(self):
      services = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
      sys.path.append(os.path.join(services, 'services'))
      global add_list
      from services.add_clients import add_list
      
def window_register(frame_nome, frame_cpf, frame_cidade):

   global select_estado
   global select_cidade

   funcoes = Funcoes()

   janela = Toplevel()

   funcoes.imports()
   funcoes.biblioteca()

   #configurações da janela
   janela.geometry('400x400')
   janela.title('registrar cliente')

   #entrys das informações
   entry_name = Entry(janela, font=('arial', 16), bg='white', fg='black')
   entry_name.pack(pady=10, fill=X)

   entry_secname = Entry(janela, font=('arial', 16), bg='white', fg='black')
   entry_secname.pack(pady=2, fill=X)

   select_estado = Combobox(janela, font=('arial', 16), values=estado, state='readonly')
   select_estado.pack(pady=2, fill=X)
   select_estado.set('Selecione o estado')
   select_estado.bind("<<ComboboxSelected>>", lambda event:funcoes.pegando_dados(select_cidade))
   
   select_cidade = Combobox(janela, font=('arial', 16), state='disabled')
   select_cidade.pack(pady=2, fill=X)
   select_cidade.set('Selecione a cidade')

   entry_cpf = Entry(janela, font=('arial', 16), bg='white', fg='black')
   entry_cpf.pack(pady=2, fill=X)


   btn = Button(janela, text='teste', font=('arial', 16), bg='white', fg='black', border=0, command=partial(add_list, janela, frame_nome, entry_name, entry_secname, frame_cpf, entry_cpf, frame_cidade, select_cidade))
   btn.pack(pady=10, fill=X)

   janela.mainloop()