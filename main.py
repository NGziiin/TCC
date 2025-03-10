import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.janelaprincipal()
        self.botões()

    def janelaprincipal(self):
        self.SetSize(1920, 1040)
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX)
        self.Maximize(True)
        self.Bind(wx.EVT_MAXIMIZE, self.on_maximize)
        self.SetTitle('Controle de estoque')
        self.Centre()

    def on_maximize(self, event):
        self.SetSize(wx.GetDisplaySize())
        self.Center()

    def botões(self):
        panel = wx.Panel(self)

        btn1 = wx.Button(panel, label='Vendas', pos=(3, 200), size=(150, 50))
        btn1.Bind(wx.EVT_BUTTON, self.teste)
        btn2 = wx.Button(panel, label='Estoque', pos=(3, 260), size=(150, 50))
        btn3 = wx.Button(panel, label='Registro de produto', pos=(3, 320), size=(150,50))
        btn4 = wx.Button(panel, label='Clientes', pos=(3, 380), size=(150, 50))

    def teste(self, event):
        wx.MessageBox("botão de teste", "informação", wx.OK | wx.ICON_INFORMATION)

def main():
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()