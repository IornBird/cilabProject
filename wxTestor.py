# not a part of project
import wx


class theFrame(wx.Frame):
    def __init__(self, title: str, size):
        super().__init__(parent=None, id=wx.ID_ANY, title=title, size=size)
        panels = [
            wx.Panel(self, size=(300, 100)),
            wx.Panel(self, size=(200, 50)),
            wx.Panel(self),
            wx.Panel(self)
        ]
        sizer = wx.GridBagSizer()
        L = [(1, 1), (0, 0), (1, 2), (2, 2)]
        S = [(3, 1), (2, 1), (1, 1), (1, 1)]
        for i, c in enumerate(panels):
            c.SetBackgroundColour(wx.Colour(*[i * 64 for f in range(3)]))
            sizer.Add(c, L[i], S[i], wx.EXPAND, 5)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(1)
        self.SetSizerAndFit(sizer)
        for c in panels:
            print(c.GetSize())


if __name__ == '__main__':
    app = wx.App()
    frame = theFrame("Title", (1024, 576))
    frame.Show()
    app.MainLoop()
