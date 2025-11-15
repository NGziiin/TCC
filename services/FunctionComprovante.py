import win32ui
import win32print
from datetime import datetime


class Comprovante:
    def __init__(self, codigovenda=None, items=None):
        print(f'dentro do functionComprovante: {items}')
        self.imprimir_comprovante_texto(codigovenda, items)

    def imprimir_comprovante_texto(self, codigovenda, items, store="Loja TCC & LTDA", phone="(62) 3451-4002", tax=0.0):
        try:
            printer_name = win32print.GetDefaultPrinter()
            hprinter = win32print.OpenPrinter(printer_name)
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)

            # Inicia o documento
            hdc.StartDoc(f"Comprovante {codigovenda}")
            hdc.StartPage()

            # Define fonte monoespaçada (para alinhamento)
            font = win32ui.CreateFont({
                "name": "Courier New",
                "height": 20,
                "weight": 400
            })
            hdc.SelectObject(font)

            # Posições iniciais
            x = 100
            y = 100
            line_h = 30

            # Cabeçalho
            hdc.TextOut(x, y, store)
            y += line_h
            hdc.TextOut(x, y, f"Telefone: {phone}")
            y += line_h
            hdc.TextOut(x, y, f"Código da venda: {codigovenda}")
            y += line_h
            hdc.TextOut(x, y, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            y += line_h * 2

            # Cabeçalho da tabela
            hdc.TextOut(x, y, "Item                 Qtd   Total")
            y += line_h
            hdc.TextOut(x, y, "-" * 35)
            y += line_h

            # Itens
            subtotal = 0.0
            for nome, qtd, preco in items:
                total_item = qtd * preco
                subtotal += total_item
                linha = f"{nome[:18]:<20} {qtd:<5} R${total_item:>6.2f}"
                hdc.TextOut(x, y, linha)
                y += line_h

            # Totais
            y += line_h
            taxa = tax
            total = subtotal + taxa

            hdc.TextOut(x, y, f"Subtotal: R${subtotal:,.2f}".replace('.', 'x').replace(',', '.').replace('x', ','))
            y += line_h
            hdc.TextOut(x, y, f"Taxa:     R${taxa:,.2f}".replace('.', 'x').replace(',', '.').replace('x', ','))
            y += line_h
            hdc.TextOut(x, y, f"Total:    R${total:,.2f}".replace('.', 'x').replace(',', '.').replace('x', ','))
            y += line_h * 2

            hdc.TextOut(x, y, "Obrigado pela preferência!")
            y += line_h
            hdc.TextOut(x, y, "Volte sempre :)")

            # Finaliza documento
            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
            win32print.ClosePrinter(hprinter)

            print("🖨️ Impressão enviada com sucesso!")

        except Exception as e:
            print(f"❌ Erro ao imprimir comprovante: {e}")
