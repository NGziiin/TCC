class Commands(object):

    def __init__(self, Ui_Form):
        self.u = Ui_Form

    def teste(self):
        print('lambda funcionou')

    def event_button(self):
        self.u.Botao_principal.clicked.connect(lambda: self.teste())