# not a part of project
import wx
from PublicFunctions import *

import wx.media

class theFrame(wx.Frame):
    def __init__(self, title: str, size):
        super().__init__(parent=None, id=wx.ID_ANY, title=title, size=size)

        sizer = wx.BoxSizer()
        self.panel = wx.media.MediaCtrl(self)

        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)

        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)

        self.panel.Load(0)
        self.panel.SetPlaybackRate(1)
        self.panel.SetVolume(1)
        self.panel.ShowPlayerControls()

        self.SetFocus()

    def OnKey(self, evt):
        assert isinstance(evt, wx.KeyEvent)
        code = evt.GetKeyCode()
        print("key down:", code)
        if code == ord(' '):
            self.Refresh()


class APane(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetFont(wx.Font(wx.FontInfo(32).FaceName("Times New Roman")))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        assert isinstance(gc, wx.GraphicsContext)
        tf = wx.AffineMatrix2D()
        gc.SetFont(self.GetFont(), wx.BLACK)
        size = self.GetTextExtent("Hello world")

        c, times = putRectangle(*size, self.GetSize())
        tf.Translate(*c)
        tf.Scale(times, times)
        gc.SetTransform(gc.CreateMatrix(tf))

        gc.DrawText("Hello world", 0, 0)


if __name__ == '__main__':
    app = wx.App()
    frame = theFrame("Title", (1024, 576))
    frame.Show()
    app.MainLoop()
