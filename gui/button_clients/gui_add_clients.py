from tkinter import *
from functools import *
from tkinter.ttk import Combobox
from tkinter import ttk
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
      
def window_register(frame_nome, frame_cpf, frame_cidade, frame_estado):

   global select_estado
   global select_cidade

   funcoes = Funcoes()

   janela = Toplevel()

   funcoes.imports()
   funcoes.biblioteca()

   funcoes = Funcoes()
   
   janela.geometry('500x450')
   janela.title('Registrar Cliente')
   janela.configure(bg='#f4f4f4')
   janela.resizable(False, False)

   # Estilo para Combobox
   style = ttk.Style()
   style.configure("TCombobox", font=('Arial', 12))

   # Título
   Label(janela, text='Cadastro de Cliente', font=('Arial', 20, 'bold'), bg='#f4f4f4', fg='#333').pack(pady=15)

   # Container principal
   container = Frame(janela, bg='#f4f4f4')
   container.pack(pady=10, padx=20, fill=BOTH, expand=True)

   # Nome
   Label(container, text='Nome:', font=('Arial', 12), bg='#f4f4f4').pack(anchor='w')
   entry_name = Entry(container, font=('Arial', 14))
   entry_name.pack(fill=X, pady=5)

   # Sobrenome
   Label(container, text='Sobrenome:', font=('Arial', 12), bg='#f4f4f4').pack(anchor='w')
   entry_secname = Entry(container, font=('Arial', 14))
   entry_secname.pack(fill=X, pady=5)

   # Estado
   Label(container, text='Estado:', font=('Arial', 12), bg='#f4f4f4').pack(anchor='w')
   select_estado = Combobox(container, font=('Arial', 12), values=estado, state='readonly')
   select_estado.set('Selecione o estado')
   select_estado.pack(fill=X, pady=5)

   # Cidade
   Label(container, text='Cidade:', font=('Arial', 12), bg='#f4f4f4').pack(anchor='w')
   select_cidade = Combobox(container, font=('Arial', 12), state='disabled')
   select_cidade.set('Selecione a cidade')
   select_cidade.pack(fill=X, pady=5)

   # Ativa cidades ao selecionar estado
   select_estado.bind("<<ComboboxSelected>>", lambda event: funcoes.pegando_dados(select_cidade))

   # CPF
   Label(container, text='CPF:', font=('Arial', 12), bg='#f4f4f4').pack(anchor='w')
   entry_cpf = Entry(container, font=('Arial', 14))
   entry_cpf.pack(fill=X, pady=5)

   # Botão de registrar
   Button(container, text='Registrar Cliente', font=('Arial', 14), bg='#4CAF50', fg='white', height=2,
          command=partial(add_list, janela, frame_nome, entry_name, entry_secname, frame_cpf, entry_cpf, frame_cidade, select_cidade, select_estado, frame_estado)).pack(pady=20, fill=X)

   janela.mainloop()