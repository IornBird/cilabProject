import wx
from gcDrawer.PaintSizer import *

class PaintObject:
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize):
        self.parent = parent
        self.pos = [*pos]
        self.minSize = [*size]
        self.size = [*self.minSize]
        self.children = list[PaintObject]()
        self.sizer = None
        self.font = wx.Font() if (parent is None) else parent.font

        self.bgColor = wx.Colour() if (parent is None) else parent.bgColor
        self.fgColor = wx.Colour() if (parent is None) else parent.fgColor

        if self.parent is not None:
            self.parent.children.append(self)

    def SetSizer(self, sizer: PaintSizer):
        self.sizer = sizer
        sizer.makeObjSizes(self)

    def SetFont(self, font: wx.Font | wx.FontInfo):
        if isinstance(font, wx.FontInfo):
            font = wx.Font(font)
        self.font = font
        for c in self.children:
            c.SetFont(font)

    def draw(self, gc: wx.GraphicsContext):
        gc.SetBrush(wx.Brush(self.bgColor))
        gc.DrawRectangle(*self.pos, *self.size)
        for c in self.children:
            c.draw(gc)


class PaintText(PaintObject):
    def __init__(self, parent: PaintObject, label: str, pos=wx.DefaultPosition, size=wx.DefaultSize):
        super().__init__(parent, pos, size)
        self.label = label
        self.resizeOnSizer = True
        if size == wx.DefaultSize:
            self.size = getTextExtent(self.font, label)

    def SetLabelText(self, text: str):
        self.label = text
        self.size = getTextExtent(self.font, text)

    def SetFont(self, font):
        if isinstance(font, wx.FontInfo):
            font = wx.Font(font)
        self.size = getTextExtent(self.font, label)
        for c in self.children:
            c.SetFont(font)

    def SetResize(self, resize: bool):
        self.resizeOnSizer = resize

    def SetSizer(self, sizer: PaintSizer):
        super().SetSizer(sizer)
        corner, times = putRectangle(*self.labelSize.Get(), self.size)
        self.pos += corner
        self.font.Scale(times)

    def draw(self, gc: wx.GraphicsContext):
        gc.SetBrush(wx.Brush(self.bgColor))
        gc.DrawRectangle(*self.pos, *self.size)

        gc.SetFont(self.font, self.fgColor)
        gc.DrawText(self.label, *self.pos)

        for c in self.children:
            c.draw(gc)


def getTextExtent(font, text):
    dc = wx.ScreenDC()
    dc.SetFont(font)
    return dc.GetTextExtent(text)
