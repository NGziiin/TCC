import customtkinter as ctk

# Configurações iniciais
ctk.set_appearance_mode("light")  # ou "dark"
ctk.set_default_color_theme("blue")

# Janela principal
janela = ctk.CTk()
janela.title("Informações do Produto")
janela.geometry("600x480")

# Título centralizado
titulo = ctk.CTkLabel(janela, text="INFORMAÇÕES DO PRODUTO", font=("Arial", 22, "bold"))
titulo.pack(pady=20)

# Container central para os dados
container = ctk.CTkFrame(janela)
container.pack(pady=10, padx=40, fill="both", expand=True)

# Dados do produto (exemplo)
produto_info = {
    "Código": "123456",
    "Nome": "Furadeira Elétrica",
    "Loja": "Ferramentas Goiás",
    "Quantidade": "10",
    "Preço Pago": "R$ 150,00",
    "Valor de Venda": "R$ 220,00",
    "Margem de Lucro": "46.7%",
    "Estoque": "7 unidades"
}

# Função para criar cada linha de informação
def criar_linha(chave, valor):
    linha = ctk.CTkFrame(container)
    linha.pack(pady=5, padx=20, fill="x")

    label_chave = ctk.CTkLabel(linha, text=f"{chave}:", width=180, anchor="e", font=("Arial", 14))
    label_chave.pack(side="left", padx=10)

    label_valor = ctk.CTkLabel(linha, text=valor, anchor="w", font=("Arial", 14))
    label_valor.pack(side="left", padx=10)

# Criar as linhas com os dados
for chave, valor in produto_info.items():
    criar_linha(chave, valor)

# Botão para fechar
botao_fechar = ctk.CTkButton(janela, text="Fechar", command=janela.destroy)
botao_fechar.pack(pady=30)

janela.mainloop()