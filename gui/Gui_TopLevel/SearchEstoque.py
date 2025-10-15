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

    # a partir daqui fica a outra janela
    @staticmethod
    def JanelaInfos():
        Interface.ConfigJanelaInfos()

    @staticmethod
    def ConfigJanelaInfos():
        for widget in Interface.janela.winfo_children():
            widget.destroy()
        Interface.janela.geometry('600x600')
        Interface.janela.title('Informações')

class Functions():

    #A FUNÇÃO ESTÁ PEGANDO AS INFORMAÇÕES DO BANCO DE DADOS ## AGORA É CRIAR A OUTRA INTERFACE QUE VAI APARECER AS INFORMAÇÕES
    #E CRIAR A FUNÇÃO DENTRO DO BANCO DE DADOS DE PEGAR TODAS AS INFORMAÇÕES DO PRODUTO ESPECIFICO.
    def DoubleClickSelect(event, tabela):
        from database.StorageRegisterDB import StorageRegisterClassDB
        item_selecionado = tabela.focus()
        valores = tabela.item(item_selecionado, 'values')
        print(f'o clique foi em {valores}')
        StorageRegisterClassDB.LoadInfosSelected(valores)
        Interface.JanelaInfos()

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