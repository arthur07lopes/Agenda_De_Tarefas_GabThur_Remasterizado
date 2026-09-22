import wx

from interface import AgendaTarefasFrame


class AgendaTarefasApp(wx.App):
    def OnInit(self):
        frame = AgendaTarefasFrame()
        frame.Show()
        return True


if __name__ == "__main__":
    app = AgendaTarefasApp()
    app.MainLoop()
