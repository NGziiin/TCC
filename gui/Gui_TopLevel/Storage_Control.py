from tkinter import *
import customtkinter as ctk
from database.StorageRegisterDB import StorageRegisterDB
from functools import partial



#JANELA DE SELEÇÃO PARA ESCOLHER SE QUER EDITAR OU EXCLUIR ITEM DO BANCO DE DADOS
def abrir_gerenciador_estoque():
    
    popup = Toplevel()
    popup.title("Gerenciar Estoque")
    popup.geometry("300x180")
    popup.configure(bg="white")
    popup.resizable(False, False)
    popup.grab_set()

    Label(popup, text="O que você deseja fazer?", font=("Arial", 14, "bold"), bg="white").pack(pady=20)

    btn_registrar = Button(popup, text="Registrar Produto", font=("Arial", 12), bg="green", fg="white", width=18,
                           command=lambda: [popup.destroy(), janela_registro()])
    btn_registrar.pack(pady=5)

    btn_editar = Button(popup, text="Editar / Excluir Produto", font=("Arial", 12), bg="orange", fg="white", width=18,
                        command=lambda: [popup.destroy(), janela_editar()])
    btn_editar.pack(pady=5)

#ESSA JANELA É A DE REGISTRAR NOVO PRODUTO NO SISTEMA
def janela_registro():
     
     janela = ctk.CTkToplevel()
     janela.title("Registrar Produto")
     janela.geometry("400x400")
     janela.resizable(False, False)
     
     titulo = ctk.CTkLabel(janela, text="Registrar Produto", font=ctk.CTkFont(size=18, weight="bold"))
     titulo.pack(pady=10)
     
     def campo(texto):
         frame = ctk.CTkFrame(janela, fg_color="transparent")
         frame.pack(fill="x", padx=20, pady=6)
         lbl = ctk.CTkLabel(frame, text=texto, anchor="w", font=ctk.CTkFont(size=13))
         lbl.pack(anchor="w")
         entry = ctk.CTkEntry(frame, font=ctk.CTkFont(size=13))
         entry.pack(fill="x", pady=4)
         return entry
     
     CodRegister = campo("Código:")
     NameRegister = campo("Nome do Produto:")
     AmountRegister = campo("Quantidade:")
     PriceRegister = campo("Valor Unitário (R$):")
     
     frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
     frame_botoes.pack(pady=10)
     
     btn_confirmar = ctk.CTkButton(frame_botoes, 
                                   text="Confirmar", 
                                   text_color='white', 
                                   fg_color="green", 
                                   hover_color="darkgreen", 
                                   width=120,
                                   command=partial(StorageRegisterDB.AddStorageDB, CodRegister, NameRegister, AmountRegister, PriceRegister, janela.destroy()))
     btn_confirmar.pack(side="left", padx=10)

     btn_cancelar = ctk.CTkButton(frame_botoes, 
                                  text="Cancelar", 
                                  text_color='white',
                                  command=lambda: janela.destroy(), 
                                  fg_color="red", 
                                  hover_color="#b81414", 
                                  width=120)
     btn_cancelar.pack(side="left", padx=10)
     janela.grab_set()

#ESSA JANELA EDITA E DELETA O PRODUTO QUE FOR SELECIONADO
def janela_editar():
    janela = ctk.CTkToplevel()
    janela.title("Editar/Excluir Produto")
    janela.geometry("400x400")
    janela.resizable(False, False)
    
    # Título
    titulo = ctk.CTkLabel(janela, text="Editar/Excluir Produto", font=ctk.CTkFont(size=18, weight="bold"))
    titulo.pack(pady=10)
    
    # Função para criar campo
    def campo(texto, valor=""):
        frame = ctk.CTkFrame(janela, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=6)
        lbl = ctk.CTkLabel(frame, text=texto, anchor="w", font=ctk.CTkFont(size=13))
        lbl.pack(anchor="w")
        entry = ctk.CTkEntry(frame, font=ctk.CTkFont(size=13))
        entry.insert(0, valor)
        entry.pack(fill="x", pady=4)
        return entry
    
    # Campos preenchíveis
    entry_codigo = campo("Código do Produto:")
    entry_nome = campo("Nome do Produto:")
    entry_qtd = campo("Quantidade:")
    entry_valor = campo("Valor Unitário (R$):")
    
    # Frame para botões
    frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
    frame_botoes.pack(pady=10)
    
    btn_salvar = ctk.CTkButton(frame_botoes, text="Salvar Alterações", 
                               text_color='white', 
                               fg_color="green", 
                               hover_color="darkgreen", 
                               width=140)
    btn_salvar.pack(side="left", padx=10)

    btn_excluir = ctk.CTkButton(frame_botoes, 
                                text="Excluir Produto", 
                                text_color='white', 
                                fg_color="orange", 
                                hover_color="#cc0e00", 
                                width=140)
    btn_excluir.pack(side="left", padx=10)

    janela.grab_set()