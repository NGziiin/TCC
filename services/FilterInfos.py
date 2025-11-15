from database.SoftwareDB import DBLog
import tkinter as tk

class LogicLog:
    def GetFilter(filtro_tipo, text_relatorio):
        filtro = filtro_tipo.get() if filtro_tipo else 'Todos'
        print(filtro)
        DBinfos = DBLog.LoadLogDB()
        LogicLog.ExibirRelatorio(DBinfos, filtro, text_relatorio)

    def ExibirRelatorio(DBinfos, filtro, text_relatorio):
        contagem = 0
        text_relatorio.config(state='normal')
        text_relatorio.delete("1.0", tk.END)
        for linha in DBinfos:
            id_, situacao, produto, marca, quantidade, data = linha

            #aplica o filtro de pesquisa
            linha_formatada = f'| {situacao} |  Produto: {produto} - Marca: {marca} - Quantidade: {int(quantidade)} - Data Inserida: {data}\n'

            if filtro == 'Todos' or situacao.strip().lower() == filtro.strip().lower():
                contagem += 1
                text_relatorio.insert(
                    tk.END,
                    linha_formatada,
                    situacao.lower().replace(' ', '')
                )
        text_relatorio.config(state='disabled') # fecha novamente o text quando terminar as mudanças do filtro