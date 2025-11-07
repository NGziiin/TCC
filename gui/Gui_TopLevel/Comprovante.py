import customtkinter as ctk
import tkinter as tk
from customtkinter import *

class ReceiptView(ctk.CTkFrame):
    def __init__(self, parent, width=480, height=680, **kwargs):
        super().__init__(parent, **kwargs)

        self.paper_width = width
        self.paper_height = height
        self.configure(fg_color="#ffffff")

        # Canvas simulando o papel do comprovante
        self.canvas = tk.Canvas(
            self, width=width, height=height,
            bg="white", highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        # Fontes do recibo
        self.font_header = ("Helvetica", 16, "bold")
        self.font_sub = ("Helvetica", 10)
        self.font_mono = ("Courier", 9)
        self.font_item = ("Helvetica", 10)
        self.font_total = ("Helvetica", 12, "bold")
        self.font_thanks = ("Helvetica", 10, "italic")

        # Exemplo estático de layout (sem funções)
        W = self.paper_width
        H = self.paper_height
        pad_x = 20
        y = 18

        # Cabeçalho fixo
        self.canvas.create_text(W/2, y, text="sistema de estoque - Lojas TCC & LTDA", font=self.font_header, anchor='n')
        y += 28
        self.canvas.create_text(W/2, y, text="Telefone: (00) 0000-0000", font=self.font_sub, anchor='n')
        y += 22
        self.canvas.create_line(pad_x, y, W - pad_x, y)
        y += 12

        # Cabeçalhos de coluna
        self.canvas.create_text(pad_x+4, y, text="Item", font=("Helvetica", 10, "bold"), anchor='w')
        self.canvas.create_text(W-120, y, text="Qtd", font=("Helvetica", 10, "bold"))
        self.canvas.create_text(W-40, y, text="Total", font=("Helvetica", 10, "bold"))
        y += 18

        # Exemplo de itens estáticos
        itens_exemplo = [
            ("Arroz Tipo 1 - Pacote 5kg", "2", "39.80"),
            ("Feijão Carioca 1kg", "1", "8.50"),
            ("Açúcar Refinado 1kg", "3", "14.25"),
            ("Óleo de Soja 900ml", "1", "7.30"),
        ]

        for item, qtd, total in itens_exemplo:
            self.canvas.create_text(pad_x+6, y, text=item, anchor='w', font=self.font_item)
            self.canvas.create_text(W-120, y, text=qtd, font=self.font_item)
            self.canvas.create_text(W-40, y, text=total, font=self.font_item)
            y += 20

        # Rodapé fixo
        footer_y = H - 80
        self.canvas.create_line(pad_x, footer_y, W - pad_x, footer_y)

        self.canvas.create_text(W-140, footer_y + 10, text="Subtotal:", anchor='e', font=self.font_sub)
        self.canvas.create_text(W-40, footer_y + 10, text="R$69.85", anchor='e', font=self.font_sub)

        self.canvas.create_text(W-140, footer_y + 30, text="Taxa:", anchor='e', font=self.font_sub)
        self.canvas.create_text(W-40, footer_y + 30, text="R$0.00", anchor='e', font=self.font_sub)

        self.canvas.create_text(W-140, footer_y + 50, text="Total:", anchor='e', font=self.font_total)
        self.canvas.create_text(W-40, footer_y + 50, text="R$69.85", anchor='e', font=self.font_total)

        self.canvas.create_text(W/4, H-28, text="Obrigado pela preferência!",
                                font=self.font_thanks, anchor='s')

        # Moldura do papel
        self.canvas.create_rectangle(2, 2, W-2, H-2, outline="#000000", width=1)


if __name__ == '__main__':
    janela = CTk()
    recibo = ReceiptView(janela)
    recibo.pack(padx=10, pady=10)
    janela.mainloop()