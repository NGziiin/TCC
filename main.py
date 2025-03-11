import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.janelaprincipal()

    def on_maximize(self, event):
        self.SetSize(wx.GetDisplaySize())
        self.Center()

    def janelaprincipal(self):

        panel_principal = wx.Panel(self)
        panel_principal.SetBackgroundColour((51, 153, 255))

        painel_esqueda = wx.Panel(panel_principal)
        painel_esqueda.SetBackgroundColour((255, 255, 255))
        direita = wx.BoxSizer(wx.VERTICAL)
        painel_esqueda.SetSize(direita)

        painel_direita = wx.Panel(panel_principal)

        self.SetSize(1920, 1040)
        self.SetMinSize((1920, 1040))
        self.Maximize(True)
        self.Bind(wx.EVT_MAXIMIZE, self.on_maximize)
        self.SetTitle('Controle de estoque')
        self.Centre()

        panel_principal.Add(direita, 1, wx.EXPAND | wx.ALL, 5)

        btn1 = wx.Button(panel_principal, label='Vendas', pos=(3, 200), size=(150, 50))
        btn1.Bind(wx.EVT_BUTTON, self.teste)
        btn2 = wx.Button(panel_principal, label='Estoque', pos=(3, 260), size=(150, 50))
        btn3 = wx.Button(panel_principal, label='Registro de produto', pos=(3, 320), size=(150,50))
        btn4 = wx.Button(panel_principal, label='Clientes', pos=(3, 380), size=(150, 50))

    def teste(self, event):
        wx.MessageBox("botão de teste", "informação", wx.OK | wx.ICON_INFORMATION)

def main():
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()