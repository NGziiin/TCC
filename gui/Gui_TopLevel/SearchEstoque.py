from customtkinter import CTk
from customtkinter import *
from tkinter import ttk

class Interface:

    def __init__(self):
        self.janela_info = CTkToplevel()
        self.WindowConfigure()
        self.MainFrame()
        self.Treeview()
        self.janela_info.mainloop()

    def WindowConfigure(self):
        self.janela_info.geometry('500x300')
        self.janela_info.title('Selecione o produto')
        self.janela_info.resizable(False, False)
        self.janela_info.grab_set()

    def MainFrame(self):
        self.frame = CTkFrame(self.janela_info, fg_color='red', width=500, height=280)
        self.frame.pack(fill='both', expand=True)
        self.LabelInfo = CTkLabel(self.janela_info, fg_color='transparent', text='⚠️ Para selecionar um item, dê 2 cliques', width=500, height=20)
        self.LabelInfo.pack(fill='x', expand=True)

    def Treeview(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TABELA2.Treeview.Heading", background='gray', foreground='white', font=('Arial', 10, 'bold'))
        style.configure('TABELA2.Treeview', background='white', foreground='black', rowheight=25, fieldbackground='white')
        style.map('TABELA2.Treeview', background=[('selected', 'lightblue')])

        self.tabela = ttk.Treeview(self.frame, columns=('Produto', 'Marca'), show='headings', style='TABELA2.Treeview')
        self.tabela.heading('Produto', text='Produto', anchor='center')
        self.tabela.heading('Marca', text='Marca', anchor='center')
        self.tabela.column('Produto', anchor="center")
        self.tabela.column('Marca', anchor='center')

        self.tabela.tag_configure('par', background='#E9EAE8')
        self.tabela.tag_configure('impar', background='#d0d0d0')

        self.tabela.pack(fill='both', expand=True)

        self.tabela.bind("<Double-1>", lambda event: Functions.DoubleClickSelect(self, event, self.tabela))
        Functions.InsertItensTable(self, self.tabela)

class InterfaceInfos:
    def __init__(self, interface: Interface, info_material: dict):
        self.interface = interface
        self.info_material = info_material
        self.ConfigJanelaInfos()
        self.FrameInfos()
        self.LabelInfos()

    def ConfigJanelaInfos(self):
        for widget in self.interface.janela_info.winfo_children():
            widget.destroy()
        self.interface.janela_info.geometry('600x480')
        self.interface.janela_info.title('Informações')
        self.interface.janela_info.resizable(False, False)

    def FrameInfos(self):
        self.Frame = CTkFrame(self.interface.janela_info, fg_color='white')
        self.Frame.pack(fill='both', expand=True)

    def LabelInfos(self):

        # Container mais largo e centralizado
        container = CTkFrame(self.Frame, fg_color='#e1e1e1', width=520, height=320)
        container.place(relx=0.5, rely=0.44, anchor='center')

        # Título
        titulo = CTkLabel(self.Frame, text="INFORMAÇÕES DO PRODUTO", font=("Arial", 20, "bold"))
        titulo.pack(pady=(20, 20))

        # Linhas de informação
        for chave, valor in self.info_material.items():
            linha = CTkFrame(container, fg_color='#B8B2B2')
            linha.pack(pady=5, padx=10, fill='x')  # Adiciona margem lateral

            label_chave = CTkLabel(linha, text=f"{chave}:", width=160, anchor='w', font=("Arial", 14, 'bold'))
            label_chave.pack(side='left', padx=(10, 10))

            label_valor = CTkLabel(linha, text=valor, anchor='w', font=("Arial", 14))
            label_valor.pack(side='left', padx=(10, 10))

        # Botão Fechar
        botao_fechar = CTkButton(self.Frame, text="Fechar", command=self.interface.janela_info.destroy)
        botao_fechar.pack(pady=(320, 20))

class Functions:
    #A FUNÇÃO ESTÁ PEGANDO AS INFORMAÇÕES DO BANCO DE DADOS ## AGORA É CRIAR A OUTRA INTERFACE QUE VAI APARECER AS INFORMAÇÕES
    #E CRIAR A FUNÇÃO DENTRO DO BANCO DE DADOS DE PEGAR TODAS AS INFORMAÇÕES DO PRODUTO ESPECIFICO.
    def DoubleClickSelect(interface: Interface, event, tabela):
        from database.StorageRegisterDB import StorageRegisterClassDB
        item_selecionado = tabela.focus()
        valores = tabela.item(item_selecionado, 'values')
        print(f'o clique foi em {valores}')
        informacoes = StorageRegisterClassDB.LoadInfosSelected(valores)
        print(f'a variável feita agora {informacoes}')
        info_material = {
            "Código": "123456",
            "Nome": "Furadeira Elétrica",
            "Loja": "Ferramentas Goiás",
            "Quantidade": "10",
            "Preço Pago": "R$ 150,00",
            "Valor de Venda": "R$ 220,00",
            "Margem de Lucro": "46.7%",
            "Estoque": "7 unidades"
        }

        InterfaceInfos(interface, info_material)

    def InsertItensTable(self, tabela):
        infos = Logic.LoadInfoDatabase(self)
        for i, linhas in enumerate(infos):
            id_, product, marca = linhas
            tag = 'par' if i % 2 == 0 else 'impar'
            tabela.insert('', 'end', values=(product, marca), tags=(tag, ))

class Logic:
    def LoadInfoDatabase(self):
        from database.StorageRegisterDB import StorageRegisterClassDB
        infosgeted = StorageRegisterClassDB.LoadSearchStorage()
        return infosgeted