from gui.Gui_TopLevel import Comprovante
import customtkinter as ctk

def AbrirComprovante(janela, dados_venda):
    janela_comprovante = ctk.CTkToplevel(janela)
    janela_comprovante.title(f"Comprovante #{dados_venda['codigo_venda']}")
    janela_comprovante.geometry("520x660")

    recibo = Comprovante.ReceiptView(janela_comprovante)
    recibo.pack(padx=10, pady=10)

    if hasattr(recibo, "render_receipt"):
        recibo.render_receipt(
            store="Minha Loja Exemplo",
            phone="(00) 0000-0000",
            items=dados_venda["itens"],
            tax=0.00
        )
