import tkinter as tk

# Simulação de um banco de dados de produtos
produtos = {
    "123": {"nome": "Caneta Azul", "preco": "R$ 2,50"},
    "456": {"nome": "Caderno 100 folhas", "preco": "R$ 12,00"},
    "789": {"nome": "Borracha", "preco": "R$ 1,00"},
}

def buscar_produto(event):
    codigo = entry_codigo.get()
    info = produtos.get(codigo)
    if info:
        label_nome.config(text=f"Nome: {info['nome']}")
        label_preco.config(text=f"Preço: {info['preco']}")
    else:
        label_nome.config(text="Nome: Produto não encontrado")
        label_preco.config(text="Preço: -")

# Interface gráfica
root = tk.Tk()
root.title("Consulta de Produto")
root.geometry('300x300')

tk.Label(root, text="Código do Produto:").pack()
entry_codigo = tk.Entry(root)
entry_codigo.pack()
entry_codigo.bind("<KeyRelease>", buscar_produto)  # Atualiza a cada tecla

label_nome = tk.Label(root, text="Nome:")
label_nome.pack()

label_preco = tk.Label(root, text="Preço:")
label_preco.pack()

root.mainloop()