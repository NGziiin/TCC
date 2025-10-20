from customtkinter import CTk
from customtkinter import *
from tkinter import ttk

class Interface:

    janela = CTk()

    def __init__(self):
        self.WindowConfigure()
        self.MainFrame()
        self.Treeview()
        self.janela.mainloop()

    def WindowConfigure(self):
        self.janela.geometry('500x300')
        self.janela.title('Selecione o produto')
        self.janela.resizable(False, False)

    def MainFrame(self):
        self.frame = CTkFrame(self.janela, fg_color='red', width=500, height=280)
        self.frame.pack(fill='both', expand=True)
        self.LabelInfo = CTkLabel(self.janela, fg_color='transparent', text='⚠️ Para selecionar um item, dê 2 cliques' , width=500, height=20)
        self.LabelInfo.pack(fill='x', expand=True)

    def Treeview(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview.Heading", background='gray', foreground='white', font=('Arial', 10, 'bold'))
        style.configure('Treeview', background='white', foreground='black', rowheight=25, fieldbackground='white')
        style.map('Treeview', background=[('selected', 'lightblue')])

        self.tabela = ttk.Treeview(self.frame, columns=('Produto', 'Marca'), show='headings')
        self.tabela.heading('Produto', text='Produto', anchor='center')
        self.tabela.heading('Marca', text='Marca', anchor='center')
        self.tabela.column('Produto', anchor="center")
        self.tabela.column('Marca', anchor='center')

        self.tabela.tag_configure('par', background='#E9EAE8')
        self.tabela.tag_configure('impar', background='#d0d0d0')

        self.tabela.pack(fill='both', expand=True)

        self.tabela.bind("<Double-1>", lambda event: Functions.DoubleClickSelect(event, self.tabela))
        Functions.InsertItensTable(self, self.tabela)

class InterfaceInfos():
    def __init__(self):
        self.ConfigJanelaInfos()
        self.FrameInfos()
        self.LabelInfos()

    def ConfigJanelaInfos(self):
        for widget in Interface.janela.winfo_children():
            widget.destroy()
        Interface.janela.geometry('600x480')
        Interface.janela.title('Informações')
        Interface.janela.resizable(False, False)

    def FrameInfos(self):
        self.Frame = CTkFrame(Interface.janela, fg_color='#e1e1e1', height=600, width=600)
        self.Frame.pack(fill='both', expand=True)

    def LabelInfos(self):
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

        # Container centralizado no meio da tela
        container = CTkFrame(self.Frame, fg_color='transparent')
        container.place(relx=0.5, rely=0.5, anchor='center')

        # Título
        titulo = CTkLabel(container, text="INFORMAÇÕES DO PRODUTO", font=("Arial", 20, "bold"))
        titulo.pack(pady=(0, 20))

        # Linhas de informação
        for chave, valor in info_material.items():
            linha = CTkFrame(container, fg_color='transparent')
            linha.pack(pady=5, fill='x')

            label_chave = CTkLabel(linha, text=f"{chave}:", width=160, anchor='e', font=("Arial", 14))
            label_chave.pack(side='left', padx=(0, 10))

            label_valor = CTkLabel(linha, text=valor, anchor='w', font=("Arial", 14))
            label_valor.pack(side='left')

        # Botão Fechar
        botao_fechar = CTkButton(container, text="Fechar", command=Interface.janela.destroy)
        botao_fechar.pack(pady=20)


class Functions():

    #A FUNÇÃO ESTÁ PEGANDO AS INFORMAÇÕES DO BANCO DE DADOS ## AGORA É CRIAR A OUTRA INTERFACE QUE VAI APARECER AS INFORMAÇÕES
    #E CRIAR A FUNÇÃO DENTRO DO BANCO DE DADOS DE PEGAR TODAS AS INFORMAÇÕES DO PRODUTO ESPECIFICO.
    def DoubleClickSelect(event, tabela):
        from database.StorageRegisterDB import StorageRegisterClassDB
        item_selecionado = tabela.focus()
        valores = tabela.item(item_selecionado, 'values')
        print(f'o clique foi em {valores}')
        StorageRegisterClassDB.LoadInfosSelected(valores)
        InterfaceInfos()

    def InsertItensTable(self, tabela):
        infos = Logic.LoadInfoDatabase(self)
        for i, linhas in enumerate(infos):
            id_, product, marca = linhas
            tag = 'par' if i % 2 == 0 else 'impar'
            tabela.insert('', 'end', values=(product, marca), tags=(tag, ))

class Logic():
    def LoadInfoDatabase(self):
        from database.StorageRegisterDB import StorageRegisterClassDB
        infosgeted = StorageRegisterClassDB.LoadSearchStorage()
        return infosgeted


if __name__ == '__main__':
    #Functions.InsertItensTable(self=True, tabela=True)
    Interface()