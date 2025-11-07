"""
Comprovante de Vendas - CustomTkinter

Como usar:
1) Instale dependências: pip install customtkinter pillow
2) Execute: python comprovante_customtkinter.py

Funcionalidades:
- Adicionar itens (descrição, quantidade, preço unitário)
- Visualizar comprovante renderizado em um Canvas (estilo receipt)
- Salvar comprovante como imagem PNG
- Imprimir (usa métodos nativos: Windows -> os.startfile(..., 'print'); mac/linux -> lp se disponível)

Observações:
- O salvamento converte o conteúdo do Canvas para PostScript e então para imagem via Pillow.
- Impressão depende das ferramentas do sistema; caso não funcione automaticamente, a imagem será salva e você poderá imprimir manualmente.

Correção aplicada: erro relacionado ao uso de width/height no método place(). Agora os parâmetros width e height são passados ao construtor dos widgets (CTkFrame), e place() é chamado apenas com x/y quando necessário — conforme exige o CustomTkinter.
"""

import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageGrab
import io
import tempfile
import os
import platform
import subprocess
from datetime import datetime

# Configurações visuais
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

WINDOW_W = 820
WINDOW_H = 700
CANVAS_W = 480
CANVAS_H = 640

class ReceiptApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Comprovante de Vendas - Salvar / Imprimir")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.resizable(False, False)

        self.items = []  # lista de tuplas (descr, qty, price)

        # Left frame: formulário e lista de itens
        left = ctk.CTkFrame(self, width=320, height=WINDOW_H-24, corner_radius=8)
        left.place(x=12, y=12)

        ctk.CTkLabel(left, text="Adicionar Item", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(12,6))

        frm = ctk.CTkFrame(left)
        frm.pack(padx=12, pady=6, fill='x')

        ctk.CTkLabel(frm, text="Descrição:").grid(row=0, column=0, sticky='w', padx=6, pady=6)
        self.entry_descr = ctk.CTkEntry(frm)
        self.entry_descr.grid(row=0, column=1, padx=6, pady=6)

        ctk.CTkLabel(frm, text="Quantidade:").grid(row=1, column=0, sticky='w', padx=6, pady=6)
        self.entry_qty = ctk.CTkEntry(frm)
        self.entry_qty.grid(row=1, column=1, padx=6, pady=6)

        ctk.CTkLabel(frm, text="Preço unitário (R$):").grid(row=2, column=0, sticky='w', padx=6, pady=6)
        self.entry_price = ctk.CTkEntry(frm)
        self.entry_price.grid(row=2, column=1, padx=6, pady=6)

        btn_add = ctk.CTkButton(left, text="Adicionar", command=self.add_item)
        btn_add.pack(pady=(6,8))

        # Treeview com itens adicionados
        self.tree = ttk.Treeview(left, columns=("qtd", "unit", "total"), show='headings', height=9)
        self.tree.heading('qtd', text='Qtd')
        self.tree.heading('unit', text='Preço Unit.')
        self.tree.heading('total', text='Total')
        self.tree.column('qtd', width=50, anchor='center')
        self.tree.column('unit', width=80, anchor='e')
        self.tree.column('total', width=80, anchor='e')
        self.tree.pack(padx=8, pady=8, fill='x')

        btn_remove = ctk.CTkButton(left, text="Remover Selecionado", command=self.remove_selected)
        btn_remove.pack(pady=(4,8))

        # Totais e ações
        self.lbl_total = ctk.CTkLabel(left, text="Total: R$ 0.00", font=ctk.CTkFont(size=14, weight='bold'))
        self.lbl_total.pack(pady=(6,12))

        btn_render = ctk.CTkButton(left, text="Atualizar Comprovante", command=self.render_receipt)
        btn_render.pack(pady=(0,6))

        # Right frame: canvas do comprovante e botões salvar/imprimir
        right = ctk.CTkFrame(self, width=460, height=WINDOW_H-24, corner_radius=8)
        right.place(x=340, y=12)

        ctk.CTkLabel(right, text="Visualização do Comprovante", font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(12,6))

        # Caixa que contém o Canvas com fundo claro (parecido com papel)
        paper_frame = ctk.CTkFrame(right, width=CANVAS_W+8, height=CANVAS_H+8)
        paper_frame.pack(pady=6)
        paper_frame.pack_propagate(False)

        # Canvas Tkinter puro para podermos usar postscript
        import tkinter as tk
        self.paper = tk.Canvas(paper_frame, width=CANVAS_W, height=CANVAS_H, bg='white', highlightthickness=0)
        self.paper.pack(padx=4, pady=4)

        # Botões de ação
        btns = ctk.CTkFrame(right)
        btns.pack(pady=8)

        self.btn_save = ctk.CTkButton(btns, text="Salvar como imagem", command=self.save_as_image)
        self.btn_save.grid(row=0, column=0, padx=8)

        self.btn_print = ctk.CTkButton(btns, text="Imprimir comprovante", command=self.print_receipt)
        self.btn_print.grid(row=0, column=1, padx=8)

        # Dados do cabeçalho (ex: loja)
        hdr = ctk.CTkFrame(right)
        hdr.pack(pady=(8,4), fill='x', padx=12)
        ctk.CTkLabel(hdr, text="Nome da Loja:").grid(row=0, column=0, sticky='w')
        self.entry_loja = ctk.CTkEntry(hdr)
        self.entry_loja.grid(row=0, column=1, padx=6)
        self.entry_loja.insert(0, "Minha Loja Exemplo")

        ctk.CTkLabel(hdr, text="Telefone: ").grid(row=1, column=0, sticky='w')
        self.entry_phone = ctk.CTkEntry(hdr)
        self.entry_phone.grid(row=1, column=1, padx=6)
        self.entry_phone.insert(0, "(00) 0000-0000")

        # Render inicial
        self.render_receipt()

    def add_item(self):
        descr = self.entry_descr.get().strip()
        try:
            qty = float(self.entry_qty.get())
        except Exception:
            messagebox.showerror("Erro", "Quantidade inválida")
            return
        try:
            price = float(self.entry_price.get())
        except Exception:
            messagebox.showerror("Erro", "Preço inválido")
            return

        if not descr:
            messagebox.showerror("Erro", "Descrição vazia")
            return

        self.items.append((descr, qty, price))
        self.tree.insert('', 'end', values=(int(qty) if qty.is_integer() else qty, f"{price:.2f}", f"{qty*price:.2f}"))
        self.entry_descr.delete(0, 'end')
        self.entry_qty.delete(0, 'end')
        self.entry_price.delete(0, 'end')
        self.update_total()

    def remove_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        idxs = [self.tree.index(s) for s in sel]
        for s in sel:
            self.tree.delete(s)
        # remove da lista items em ordem inversa
        for i in sorted(idxs, reverse=True):
            if i < len(self.items):
                self.items.pop(i)
        self.update_total()
        self.render_receipt()

    def update_total(self):
        total = sum(qty*price for _, qty, price in self.items)
        self.lbl_total.configure(text=f"Total: R$ {total:.2f}")

    def render_receipt(self):
        # limpa canvas
        self.paper.delete('all')

        # parâmetros de layout dentro do papel
        pad_x = 20
        y = 18
        line_h = 18

        loja = self.entry_loja.get().strip()
        phone = self.entry_phone.get().strip()

        # Cabeçalho
        self.paper.create_text(CANVAS_W/2, y, text=loja, font=("Helvetica", 16, "bold"))
        y += 28
        self.paper.create_text(CANVAS_W/2, y, text=f"Telefone: {phone}", font=("Helvetica", 10))
        y += 22
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.paper.create_text(CANVAS_W - pad_x - 10, y, text=now, anchor='e', font=("Courier", 9))
        y += 18
        self.paper.create_line(pad_x, y, CANVAS_W - pad_x, y)
        y += 12

        # Itens header
        self.paper.create_text(pad_x+10, y, text="Item", anchor='w', font=("Helvetica", 10, 'bold'))
        self.paper.create_text(CANVAS_W-120, y, text="Qtd", font=("Helvetica", 10, 'bold'))
        self.paper.create_text(CANVAS_W-60, y, text="Total", font=("Helvetica", 10, 'bold'))
        y += line_h

        # Items
        for descr, qty, price in self.items:
            # limitar linhas longas
            max_chars = 28
            parts = [descr[i:i+max_chars] for i in range(0, len(descr), max_chars)]
            for pidx, part in enumerate(parts):
                if pidx == 0:
                    self.paper.create_text(pad_x+6, y, text=part, anchor='w', font=("Helvetica", 10))
                    self.paper.create_text(CANVAS_W-120, y, text=(int(qty) if qty.is_integer() else qty), font=("Helvetica", 10))
                    self.paper.create_text(CANVAS_W-60, y, text=f"{qty*price:.2f}", font=("Helvetica", 10))
                else:
                    self.paper.create_text(pad_x+6, y, text=part, anchor='w', font=("Helvetica", 10))
                y += line_h
            # espaço entre itens
            y += 2
            if y > CANVAS_H - 80:
                self.paper.create_text(CANVAS_W/2, CANVAS_H - 40, text="--- CONTINUA EM OUTRO COMPROVANTE ---", font=("Helvetica", 9))
                break

        # Totais
        y_total = CANVAS_H - 80
        self.paper.create_line(pad_x, y_total, CANVAS_W - pad_x, y_total)
        y_total += 8
        subtotal = sum(qty*price for _, qty, price in self.items)
        tax = 0.0
        total = subtotal + tax
        self.paper.create_text(CANVAS_W-140, y_total, text="Subtotal:", anchor='e', font=("Helvetica", 10))
        self.paper.create_text(CANVAS_W-40, y_total, text=f"{subtotal:.2f}", anchor='e', font=("Helvetica", 10))
        y_total += line_h
        self.paper.create_text(CANVAS_W-140, y_total, text="Taxa:", anchor='e', font=("Helvetica", 10))
        self.paper.create_text(CANVAS_W-40, y_total, text=f"{tax:.2f}", anchor='e', font=("Helvetica", 10))
        y_total += line_h
        self.paper.create_text(CANVAS_W-140, y_total, text="Total:", anchor='e', font=("Helvetica", 12, 'bold'))
        self.paper.create_text(CANVAS_W-40, y_total, text=f"{total:.2f}", anchor='e', font=("Helvetica", 12, 'bold'))

        # rodapé
        self.paper.create_text(CANVAS_W/2, CANVAS_H-28, text="Obrigado pela preferência!", font=("Helvetica", 10, 'italic'))

        self.update_total()

    def save_as_image(self):
        # salva o canvas como imagem. tenta PostScript -> PIL, senão captura a região da tela
        try:
            # gerar postscript
            ps = self.paper.postscript(colormode='color')
            # PIL costuma abrir PS via BytesIO mas requer Ghostscript instalado no sistema para conversão
            # tentamos abrir; caso falhe, usamos ImageGrab
            im = None
            try:
                im = Image.open(io.BytesIO(ps.encode('utf-8')))
            except Exception:
                im = None
        except Exception:
            im = None

        if im is None:
            try:
                self.update()
                x = self.paper.winfo_rootx()
                y = self.paper.winfo_rooty()
                x1 = x + self.paper.winfo_width()
                y1 = y + self.paper.winfo_height()
                im = ImageGrab.grab(bbox=(x, y, x1, y1))
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao capturar imagem do comprovante: {e}")
                return

        # forçar RGB
        im = im.convert('RGB')

        # salvar em arquivo perguntando local
        from tkinter.filedialog import asksaveasfilename
        fpath = asksaveasfilename(defaultextension='.png', filetypes=[('PNG Image','*.png')], title='Salvar comprovante como...')
        if not fpath:
            return
        try:
            im.save(fpath, 'PNG')
            messagebox.showinfo("Salvo", f"Comprovante salvo em:{fpath}")
            self._last_saved = fpath
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar arquivo: {e}")

    def print_receipt(self):
        # tenta imprimir o arquivo salvo; se não existir, salva em temp e imprime
        try:
            path = getattr(self, '_last_saved', None)
            if not path or not os.path.exists(path):
                # salva em temporário
                fd, tmp_path = tempfile.mkstemp(suffix='.png')
                os.close(fd)
                # gerar imagem via captura de tela
                self.update()
                x = self.paper.winfo_rootx()
                y = self.paper.winfo_rooty()
                x1 = x + self.paper.winfo_width()
                y1 = y + self.paper.winfo_height()
                im = ImageGrab.grab(bbox=(x, y, x1, y1))
                im = im.convert('RGB')
                im.save(tmp_path, 'PNG')
                path = tmp_path

            sys_plat = platform.system()
            if sys_plat == 'Windows':
                try:
                    os.startfile(path, "print")
                    messagebox.showinfo("Impressão", "Enviado para a impressora padrão (Windows).")
                    return
                except Exception:
                    pass
            elif sys_plat == 'Darwin':
                try:
                    subprocess.run(["lp", path], check=True)
                    messagebox.showinfo("Impressão", "Enviado para a impressora (macOS).")
                    return
                except Exception:
                    pass
            else:
                try:
                    subprocess.run(["lp", path], check=True)
                    messagebox.showinfo("Impressão", "Enviado para a impressora (lp).")
                    return
                except Exception:
                    pass

            messagebox.showwarning("Impressão", f"Não foi possível imprimir automaticamente. O arquivo de imagem está em:{path}Você pode abrir e imprimir manualmente.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na tentativa de impressão: {e}")

if __name__ == '__main__':
    app = ReceiptApp()
    app.mainloop()
