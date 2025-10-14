from customtkinter import CTk
from customtkinter import *
from tkinter import ttk
from functools import partial


class Interface:
    def __init__(self):
        self.janela = CTk()
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
        self.tabela.heading('Produto', text='Produto')
        self.tabela.heading('Marca', text='Marca')

        for i in range(50):
            tag = 'par' if i % 2 == 0 else 'impar'
            self.tabela.insert('', 'end', values=(f'produto {i}', f'marca {i}'), tags=(tag, ))

        self.tabela.tag_configure('par', background='#E9EAE8')
        self.tabela.tag_configure('impar', background='#d0d0d0')

        self.tabela.bind("<Double-1>", lambda event: Functions.DoubleClickSelect(event, tabela))

        self.tabela.pack(fill='both', expand=True)

class Functions():
    def DoubleClickSelect(event, tabela):
        print('evento funcionando')
        item_selecionado = tabela.focus()
        valores = tabela.item(item_selecionado, 'values')
        print(f'o clique foi em {valores}')


if __name__ == '__main__':
    Interface()