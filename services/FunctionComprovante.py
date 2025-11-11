import tkinter as tk
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas

class Save:
    def __init__(self, canvas_widget):
        self.canvas = canvas_widget
        self.salvar_comprovante_png()
        self.gerar_pdf()

    def salvar_comprovante_png(self):
        from PIL import ImageGrab
        self.canvas.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = x + self.canvas.winfo_width()
        h = y + self.canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x, y, w, h))
        img.save("comprovante.png")

    def gerar_pdf(self):
        from reportlab.pdfgen import canvas
        c = canvas.Canvas("comprovante.pdf", pagesize=(520, 680))
        c.drawImage("comprovante.png", 0, 0, width=520, height=680)
        c.save()


class Imprimir:
    def __init__(self):
        self.imprimir_pdf()

    def imprimir_pdf(self):
        import os
        import platform

        if platform.system() == "Windows":
            os.startfile("comprovante.pdf", "print")
        elif platform.system() == "Darwin":  # macOS
            os.system("lp comprovante.pdf")
        else:  # Linux
            os.system("lpr comprovante.pdf")
