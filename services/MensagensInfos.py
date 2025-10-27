class LogicLog:
    def GetFilter(filtro_tipo):
        SearchAcordFilter = filtro_tipo.get()
        print(SearchAcordFilter)

        #aqui é onde infiltra de acordo com a escolha para colocar na tela
        match SearchAcordFilter:
            case 'Todos':
                LogicLog.LogicTodos()
            case 'Adicionados':
                pass
            case 'Removidos':
                pass
            case 'Vendidos':
                pass
            case 'Estoque Baixo':
                pass

    def LogicTodos():
        print('DEBUG Cheguei no lÓGIC TODOS')