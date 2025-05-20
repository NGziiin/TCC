from tkinter import *
from tkinter import ttk

class ClienteUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizar Cliente")
        self.root.geometry("420x450")
        self.root.configure(bg="#f0f4f7")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TCombobox", padding=6, font=('Segoe UI', 11))

        # Título
        Label(self.root, text="Informações do Cliente", font=("Segoe UI", 16, "bold"),
              bg="#f0f4f7", fg="#333").pack(pady=15)

        # Combobox para seleção do cliente
        frame_combo = Frame(self.root, bg="#f0f4f7")
        frame_combo.pack(pady=10)

        Label(frame_combo, text="Selecionar cliente:", font=("Segoe UI", 11), bg="#f0f4f7").pack(anchor="w")
        self.var_cliente = StringVar()
        self.combo = ttk.Combobox(frame_combo, textvariable=self.var_cliente, state="readonly", width=35)
        self.combo['values'] = ["Exemplo 1", "Exemplo 2", "Exemplo 3"]  # Substitua com os nomes reais
        self.combo.set("Selecione um cliente")
        self.combo.pack(pady=5)

        # Área das informações
        self.info_frame = Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        self.info_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.campos = ["Nome", "Sobrenome", "Cidade", "Estado", "CPF"]
        self.labels = {}

        for campo in self.campos:
            row = Frame(self.info_frame, bg="#ffffff")
            row.pack(anchor="w", fill="x", pady=5, padx=10)

            label_nome = Label(row, text=f"{campo}:", width=12, anchor="w", bg="#ffffff",
                               font=("Segoe UI", 11, "bold"))
            label_nome.pack(side="left")

            label_valor = Label(row, text="---", anchor="w", bg="#ffffff", font=("Segoe UI", 11))
            label_valor.pack(side="left", fill="x", expand=True)

            self.labels[campo] = label_valor

        # Botão de Visualizar
        ttk.Button(self.root, text="Visualizar", command=self.visualizar_cliente).pack(pady=10)

    def visualizar_cliente(self):
        # Você irá implementar essa parte com base no nome selecionado
        # Aqui vou apenas preencher os campos com textos fixos como exemplo
        dados_exemplo = {
            "Nome": "Maria",
            "Sobrenome": "Oliveira",
            "Cidade": "Recife",
            "Estado": "PE",
            "CPF": "000.111.222-33"
        }

        for campo in self.campos:
            self.labels[campo].config(text=dados_exemplo.get(campo, "---"))

def StartUI():
    root = Tk()
    app = ClienteUI(root)
    root.mainloop()