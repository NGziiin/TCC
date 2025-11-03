import tkinter as tk

def ajustar_largura(event):
    texto = entry.get()
    nova_largura = max(10, len(texto))  # largura mínima de 10 caracteres
    entry.config(width=nova_largura)

root = tk.Tk()
root.title("Entry que cresce")

entry = tk.Entry(root, width=10, font=("Arial", 12))
entry.pack(padx=20, pady=20)

# Detecta cada tecla liberada e ajusta a largura
entry.bind("<KeyRelease>", ajustar_largura)

root.mainloop()
