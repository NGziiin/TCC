from tkinter import *

def janelainicial(frameinfo):

    # Frame principal
    main_frame = Frame(frameinfo, bg='#F8FAFC')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Título
    Label(main_frame, text='Resumo do Sistema', font=('Arial', 22, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w', pady=(0, 20))

    # Frame de indicadores
    frame_indicadores = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_indicadores.pack(fill='x', pady=10)

    # Produto registrado
    frame_produtos = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_produtos.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_produtos, text='Produtos Registrados', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_produtos, text='245', font=('Arial', 16), bg='#f0f0f0', fg='blue').pack(pady=(5, 10))

    # Vendas realizadas
    frame_vendas = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_vendas.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_vendas, text='Vendas Realizadas', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_vendas, text='158', font=('Arial', 16), bg='#f0f0f0', fg='green').pack(pady=(5, 10))

    # Estoque baixo
    frame_estoque_baixo = Frame(frame_indicadores, bg='#f0f0f0', bd=2, relief='groove')
    frame_estoque_baixo.pack(side='left', expand=True, fill='both', padx=5)
    Label(frame_estoque_baixo, text='Estoque Baixo', font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(10,0))
    Label(frame_estoque_baixo, text='12 produtos', font=('Arial', 16), bg='#f0f0f0', fg='red').pack(pady=(5, 10))

    # Avisos / Notificações
    frame_avisos = Frame(main_frame, bg=main_frame.cget('bg'))
    frame_avisos.pack(fill='both', expand=True, pady=(20, 0))

    Label(frame_avisos, text='Avisos Importantes:', font=('Arial', 14, 'bold'), bg=main_frame.cget('bg')).pack(anchor='w')

    text_avisos = Text(frame_avisos, height=6, font=('Arial', 12), bg='#fdfdfd', wrap='word')
    text_avisos.pack(fill='both', expand=True, pady=5)

    avisos_exemplo = [
        "⚠️ Produto 'Borracha' está com estoque crítico (2 unidades).",
        "✅ Nova venda registrada: Caneta Azul - 20 unidades.",
        "📦 Produto 'Apontador' foi adicionado com sucesso."
    ]

    for aviso in avisos_exemplo:
        text_avisos.insert(END, '\n' + aviso + '\n\n')

    text_avisos.config(state='disabled')