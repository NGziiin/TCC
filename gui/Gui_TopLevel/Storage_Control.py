import tkinter as tk
import customtkinter as ctk
from database.SoftwareDB import StorageRegisterClassDB, EditProduct
from functools import partial
from services.EditProduct import LogicProduto

#JANELA DE SELEÇÃO PARA ESCOLHER SE QUER EDITAR OU EXCLUIR ITEM DO BANCO DE DADOS
def abrir_gerenciador_estoque():
    popup = tk.Toplevel()
    largura = 340
    altura = 260
    centralizar_janela(popup, largura, altura)
    popup.title("Gerenciar Estoque")
    popup.configure(bg="#F4F5F7")
    popup.resizable(False, False)
    popup.overrideredirect(True)
    popup.grab_set()

    # Frame principal
    frame = tk.Frame(
        popup,
        bg="white",
        bd=0,
        highlightthickness=1,
        highlightbackground="#D0D0D0"
    )
    frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=200)

    # Título
    title = tk.Label(
        frame,
        text="O que você deseja fazer?",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#333"
    )
    title.pack(pady=(15, 15))

    # ---------- Função de hover ----------
    def hover_enter(btn, color):
        btn.config(bg=color)

    def hover_leave(btn, color):
        btn.config(bg=color)

    # Botão registrar
    btn_registrar = tk.Button(
        frame,
        text="Registrar Produto",
        font=("Segoe UI", 11),
        bg="#27AE60",
        fg="white",
        activeforeground="white",
        activebackground="#1F8F50",
        bd=0,
        relief="flat",
        width=22,
        height=1,
        command=lambda: [popup.destroy(), janela_registro()]
    )
    btn_registrar.pack(pady=5)

    btn_registrar.bind("<Enter>", lambda e: hover_enter(btn_registrar, "#1F8F50"))
    btn_registrar.bind("<Leave>", lambda e: hover_leave(btn_registrar, "#27AE60"))

    # Botão editar
    btn_editar = tk.Button(
        frame,
        text="Editar / Excluir Produto",
        font=("Segoe UI", 11),
        bg="#F39C12",
        fg="white",
        activeforeground="white",
        activebackground="#D98207",
        bd=0,
        relief="flat",
        width=22,
        height=1,
        command=lambda: [popup.destroy(), janela_editar()]
    )
    btn_editar.pack(pady=5)

    btn_editar.bind("<Enter>", lambda e: hover_enter(btn_editar, "#D98207"))
    btn_editar.bind("<Leave>", lambda e: hover_leave(btn_editar, "#F39C12"))

    btn_cancelar = tk.Button(
        frame,
        text='Cancelar',
        font=("Segoe UI", 11),
        bg='#B22222',
        fg="white",
        activebackground='#F08080',
        activeforeground='white',
        bd=0,
        relief='flat',
        width=22,
        height=1,
        command=lambda : popup.destroy()
    )
    btn_cancelar.pack(pady=5)

    btn_cancelar.bind("<Enter>", lambda e: hover_enter(btn_cancelar, "#F08080"))
    btn_cancelar.bind("<Leave>", lambda e: hover_leave(btn_cancelar, '#B22222'))


#ESSA JANELA É A DE REGISTRAR NOVO PRODUTO NO SISTEMA
def janela_registro():
    janela = ctk.CTkToplevel()
    janela.title("Registrar Produto")
    altura = 550
    largura = 400
    centralizar_janela(janela, largura, altura)
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

    # Campos de entrada
    NameRegister = campo("Nome do Produto:")
    MarcaRegister = campo("Marca:")
    AmountRegister = campo("Quantidade:")
    PriceRegister = campo("Valor Unitário (R$):")

    # ComboBox para margem de lucro
    frame_margem = ctk.CTkFrame(janela, fg_color="transparent")
    frame_margem.pack(anchor='w', padx=18, pady=6, ipadx='40')
    lbl_margem = ctk.CTkLabel(frame_margem, text="Margem de Lucro (%):", anchor="w", font=ctk.CTkFont(size=13))
    lbl_margem.pack(anchor="w")
    opções_margem = [f'{i}%' for i in range(0, 101, 5)]
    MargemRegister = ctk.CTkComboBox(frame_margem, values=opções_margem, font=ctk.CTkFont(size=13), state='readonly')
    MargemRegister.set("SELECIONE UMA OPÇÃO")  # valor padrão
    MargemRegister.pack(anchor='w', pady=4, fill='x')

    # Botões
    frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
    frame_botoes.pack(pady=10)

    btn_confirmar = ctk.CTkButton(frame_botoes,
                                  text="Confirmar",
                                  text_color='white',
                                  fg_color="green",
                                  hover_color="darkgreen",
                                  width=120,
                                  command=partial(StorageRegisterClassDB.AddStorageDB, NameRegister, AmountRegister, PriceRegister, MarcaRegister, MargemRegister, janela))
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
    # STRINGVAR
    VarCod = tk.StringVar(value=None)
    VarName = tk.StringVar()
    VarMarca = tk.StringVar()
    VarQTD = tk.StringVar()
    VarPreco = tk.StringVar()

    # ________________________________
    janela = ctk.CTkToplevel()
    janela.title("Registrar Produto")
    largura = 400
    altura = 550
    centralizar_janela(janela, largura, altura)
    janela.resizable(False, False)

    titulo = ctk.CTkLabel(janela, text="Registrar Produto", font=ctk.CTkFont(size=18, weight="bold"))
    titulo.pack(pady=10)

    def campo(texto):
        frame = ctk.CTkFrame(janela, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=6)
        lbl = ctk.CTkLabel(frame, text=texto, anchor="w", font=ctk.CTkFont(size=13))
        lbl.pack(anchor="w")
        entry = ctk.CTkEntry(frame, font=ctk.CTkFont(size=13), state='disabled', fg_color='#CDC9C9')
        entry.pack(fill="x", pady=4)
        return entry

    # Campos de entrada
    CodProduto = campo('Código do produto:')
    CodProduto.configure(state='normal', fg_color='white', textvariable=VarCod)
    NameRegister = campo("Nome do Produto:")
    NameRegister.configure(textvariable=VarName)
    MarcaRegister = campo("Marca:")
    MarcaRegister.configure(textvariable=VarMarca)
    AmountRegister = campo("Quantidade:")
    AmountRegister.configure(textvariable=VarQTD)
    PriceRegister = campo("Valor de Compra (R$):")
    PriceRegister.configure(textvariable=VarPreco)

    # ComboBox para margem de lucro
    frame_margem = ctk.CTkFrame(janela, fg_color="transparent")
    frame_margem.pack(anchor='w', padx=18, pady=6, ipadx='40')
    lbl_margem = ctk.CTkLabel(frame_margem, text="Margem de Lucro (%):", anchor="w", font=ctk.CTkFont(size=13))
    lbl_margem.pack(anchor="w")
    opções_margem = [f'{i}%' for i in range(0, 101, 5)]
    MargemRegister = ctk.CTkComboBox(frame_margem, values=opções_margem, font=ctk.CTkFont(size=13), state='readonly')
    MargemRegister.set("Selecione uma opção")  # valor padrão
    MargemRegister.pack(anchor='w', pady=4, fill='x')

    # Botões
    frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
    frame_botoes.pack(pady=10)
    
    btn_salvar = ctk.CTkButton(frame_botoes, text="Salvar Alterações", 
                               text_color='white', 
                               fg_color="green",
                               command= lambda: EditProduct.UpdateInDB(VarCod, VarName, VarMarca, VarPreco, VarQTD, MargemRegister, janela),
                               hover_color="darkgreen", 
                               width=140)
    btn_salvar.pack(side="left", padx=10)

    btn_excluir = ctk.CTkButton(frame_botoes, 
                                text="Excluir Produto", 
                                text_color='white', 
                                fg_color="orange",
                                command= lambda: EditProduct.DeleteProductDB(VarCod, VarName, VarMarca, VarPreco, VarQTD, MargemRegister, NameRegister, MarcaRegister, AmountRegister, PriceRegister),
                                hover_color="#cc0e00", 
                                width=140)
    btn_excluir.pack(side="left", padx=10)

    CodProduto.bind("<KeyRelease>",
                    lambda event: LogicProduto.autopreenchimento(event, VarCod, VarName, VarMarca, VarPreco, VarQTD, NameRegister, MarcaRegister, AmountRegister, PriceRegister))

    janela.grab_set()

##aqui ficam as funções
#CENTRALIZA AS JANELAS
def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()

    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()

    x = (screen_width // 2) - (largura // 2)
    y = (screen_height // 2) - (altura // 2)

    janela.geometry(f"{largura}x{altura}+{x}+{y}")