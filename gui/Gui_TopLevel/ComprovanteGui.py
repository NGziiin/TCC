import customtkinter as ctk
import tkinter as tk
from datetime import datetime


class InterfaceComprovante:
    def __init__(self, items=None, codigovenda=None, store="Loja TCC & LTDA", phone="(62) 3451-4002", tax=0.0):
        ctk.set_appearance_mode('light')
        self.janela = ctk.CTk()
        self.janela.title("Comprovante de Venda")
        self.janela.geometry("520x680")
        self.janela.configure(fg_color="white")

        self.paper_width = 480
        self.paper_height = 640
        self.tax = tax
        self.store = store
        self.phone = phone
        self.codigovenda = codigovenda
        self.items = items if items else []

        self._montar_interface()
        self.run()

    def _montar_interface(self):
        # Canvas simulando o papel do comprovante
        self.canvas = tk.Canvas(
            self.janela, width=self.paper_width, height=self.paper_height,
            bg="white", highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        # ===== MENU SUPERIOR =====
        self.menu = tk.Menu(self.janela)

        # Submenu de opções
        self.opções = tk.Menu(self.menu, tearoff=0)
        self.opções.add_command(label='Salvar', command=lambda: print("Salvar comprovante"))
        self.opções.add_command(label='Imprimir', command=lambda: print("Imprimir comprovante"))
        self.opções.add_separator()
        self.opções.add_command(label='Sair', command=self.janela.quit)

        # Adiciona o submenu à barra principal
        self.menu.add_cascade(label='Opções', menu=self.opções)

        # 🔹 IMPORTANTE: adiciona o menu à janela
        self.janela.config(menu=self.menu)

        # Fontes
        self.font_header = ("Helvetica", 16, "bold")
        self.font_sub = ("Helvetica", 10)
        self.font_mono = ("Courier", 9)
        self.font_item = ("Helvetica", 10)
        self.font_total = ("Helvetica", 12, "bold")
        self.font_thanks = ("Helvetica", 10, "italic")

        # Renderiza o comprovante automaticamente
        self._render_receipt()

    def _render_receipt(self):
        W = self.paper_width
        H = self.paper_height
        pad_x = 20
        y = 18
        line_h = 18

        # Cabeçalho
        self.canvas.create_text(W / 2, y, text=self.store, font=self.font_header, anchor='n')
        y += 20
        self.canvas.create_text(W / 2, y, text=f"Telefone: {self.phone}", font=self.font_sub, anchor='n')
        y += 26
        self.canvas.create_text(W / 20, y, text=self.codigovenda, font=self.font_mono, anchor='w')

        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.canvas.create_text(W - pad_x - 10, y, text=now, anchor='e', font=self.font_mono)
        y += 8
        self.canvas.create_line(pad_x, y, W - pad_x, y)
        y += 12

        # Cabeçalhos de coluna
        self.canvas.create_text(pad_x + 4, y, text="Item", font=("Helvetica", 10, "bold"), anchor='w')
        self.canvas.create_text(W - 120, y, text="Qtd", font=("Helvetica", 10, "bold"))
        self.canvas.create_text(W - 40, y, text="Total", font=("Helvetica", 10, "bold"))
        y += line_h

        # Itens
        max_chars = 34
        for descr, qty, unit in self.items:
            total_line = qty * unit
            self.canvas.create_text(pad_x + 6, y, text=str(descr)[:max_chars], anchor='w', font=self.font_item)
            self.canvas.create_text(W - 120, y, text=str(int(qty)), font=self.font_item)
            self.canvas.create_text(
                W - 40, y,
                text=f"R${total_line:,.2f}".replace('.', 'x').replace(',', '.').replace('x', ','),
                font=self.font_item
            )
            y += line_h + 2

        # Rodapé
        footer_y = H - 80
        self.canvas.create_line(pad_x, footer_y, W - pad_x, footer_y)

        subtotal = sum(q * unit for _, q, unit in self.items)
        y_total = footer_y + 10
        self.canvas.create_text(W - 140, y_total, text="Subtotal:", anchor='e', font=self.font_sub)
        self.canvas.create_text(W - 40, y_total,
                                text=f"R${subtotal:,.2f}".replace('.', 'x').replace(',', '.').replace('x', ','),
                                anchor='e', font=self.font_sub)
        y_total += line_h
        self.canvas.create_text(W - 140, y_total, text="Taxa:", anchor='e', font=self.font_sub)
        self.canvas.create_text(W - 40, y_total,
                                text=f"R${self.tax:,.2f}".replace('.', 'x').replace(',', '.').replace('x', ','),
                                anchor='e', font=self.font_sub)
        y_total += line_h

        total = subtotal + self.tax
        self.canvas.create_text(W - 140, y_total, text="Total:", anchor='e', font=self.font_total)
        self.canvas.create_text(W - 40, y_total,
                                text=f"R${total:,.2f}".replace('.', 'x').replace(',', '.').replace('x', ','),
                                anchor='e', font=self.font_total)

        self.canvas.create_text(W / 4, H - 30, text="Obrigado pela preferência!",
                                font=self.font_thanks, anchor='s')

        # Moldura do papel
        self.canvas.create_rectangle(2, 2, W - 2, H - 2, outline="#000000", width=1)

    def run(self):
        self.janela.mainloop()


if __name__ == '__main__':
    InterfaceComprovante(codigovenda='1c261a8cf7')
