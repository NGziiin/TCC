import tkinter as tk
from tkinter import ttk


def ao_dar_dois_cliques(event):
    item_selecionado = tree.focus()  # pega o ID do item selecionado
    valores = tree.item(item_selecionado, 'values')  # pega os valores
    print("Você clicou duas vezes em:", valores)

root = tk.Tk()
root.geometry("500x300")

# Estilo personalizado
style = ttk.Style()
style.theme_use("default")

# Cor do cabeçalho
style.configure("Treeview.Heading", background="gray", foreground="white", font=('Arial', 10, 'bold'))

# Cor das linhas
style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")

# Cor alternada (zebra)
style.map("Treeview", background=[('selected', 'lightblue')])

tree = ttk.Treeview(root, columns=('Nome', 'Idade'), show='headings')
tree.heading('Nome', text='Nome')
tree.heading('Idade', text='Idade')

# Inserindo com cores alternadas
for i in range(20):
    tag = 'par' if i % 2 == 0 else 'impar'
    tree.insert('', 'end', values=(f'Pessoa {i}', 20 + i), tags=(tag,))

# Definindo cores das tags
tree.tag_configure('par', background='#f0f0f0')
tree.tag_configure('impar', background='#d0d0d0')

tree.pack(fill='both', expand=True)

tree.bind("<Double-1>", ao_dar_dois_cliques)

root.mainloop()
