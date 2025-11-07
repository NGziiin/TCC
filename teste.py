import customtkinter as ctk
import tkinter as tk
from datetime import datetime

class ReceiptView(ctk.CTkFrame):
    def __init__(self, parent, width=480, height=640, **kwargs):
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

    def clear(self):
        self.canvas.delete("all")

    def render_receipt(self, store="Minha Loja Exemplo", phone="(00) 0000-0000",
                       items=None, tax=0.0):
        if items is None:
            items = []

        self.clear()
        W = self.paper_width
        H = self.paper_height
        pad_x = 20
        y = 18
        line_h = 18

        # Cabeçalho
        self.canvas.create_text(W/2, y, text=store, font=self.font_header, anchor='n')
        y += 28
        self.canvas.create_text(W/2, y, text=f"Telefone: {phone}", font=self.font_sub, anchor='n')
        y += 22

        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.canvas.create_text(W - pad_x - 10, y, text=now, anchor='e', font=self.font_mono)
        y += 8
        self.canvas.create_line(pad_x, y, W - pad_x, y)
        y += 12

        # Cabeçalhos de coluna
        self.canvas.create_text(pad_x+4, y, text="Item", font=("Helvetica", 10, "bold"), anchor='w')
        self.canvas.create_text(W-120, y, text="Qtd", font=("Helvetica", 10, "bold"))
        self.canvas.create_text(W-40, y, text="Total", font=("Helvetica", 10, "bold"))
        y += line_h

        # Itens
        max_chars = 34
        for descr, qty, unit in items:
            total_line = qty * unit
            self.canvas.create_text(pad_x+6, y, text=str(descr)[:max_chars], anchor='w', font=self.font_item)
            self.canvas.create_text(W-120, y, text=str(int(qty)), font=self.font_item)
            self.canvas.create_text(W-40, y, text=f"{total_line:.2f}", font=self.font_item)
            y += line_h + 2

        # Rodapé
        footer_y = H - 80
        self.canvas.create_line(pad_x, footer_y, W - pad_x, footer_y)

        subtotal = sum(q*unit for _, q, unit in items)
        y_total = footer_y + 10
        self.canvas.create_text(W-140, y_total, text="Subtotal:", anchor='e', font=self.font_sub)
        self.canvas.create_text(W-40, y_total, text=f"{subtotal:.2f}", anchor='e', font=self.font_sub)
        y_total += line_h
        self.canvas.create_text(W-140, y_total, text="Taxa:", anchor='e', font=self.font_sub)
        self.canvas.create_text(W-40, y_total, text=f"{tax:.2f}", anchor='e', font=self.font_sub)
        y_total += line_h

        total = subtotal + tax
        self.canvas.create_text(W-140, y_total, text="Total:", anchor='e', font=self.font_total)
        self.canvas.create_text(W-40, y_total, text=f"{total:.2f}", anchor='e', font=self.font_total)

        self.canvas.create_text(W/2, H-28, text="Obrigado pela preferência!",
                                font=self.font_thanks, anchor='s')

        # Moldura do papel
        self.canvas.create_rectangle(2, 2, W-2, H-2, outline="#000000", width=1)


# Teste isolado
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("520x660")
    rv = ReceiptView(root)
    rv.pack(padx=10, pady=10)

    items = [
        ("Arroz Tipo 1 - Pacote 5kg", 2, 19.90),
        ("Feijão Carioca 1kg", 1, 8.50),
        ("Açúcar Refinado 1kg", 3, 4.75),
        ("Óleo de Soja 900ml", 1, 7.30),
    ]
    rv.render_receipt(items=items)
    root.mainloop()
