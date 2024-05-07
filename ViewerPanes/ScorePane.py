import wx
from PublicFunctions import *


class ScorePane(wx.Panel):
    """
    A panel that shows score and times of violating rules of a contestant
    """
    def __init__(self, parent, isBlue, scores):
        super().__init__(parent)
        self.SetFont(wx.Font(36, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.color = wx.BLUE if isBlue else wx.RED
        self.scores = scores
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.numberBoard = wx.Panel(self, style=wx.FULL_REPAINT_ON_RESIZE)
        if True:
            self.numberBoard.SetBackgroundStyle(wx.BG_STYLE_PAINT)
            self.numberBoard.SetBackgroundColour(wx.Colour(192, 192, 192))
            self.numberBoard.Bind(wx.EVT_PAINT, self.OnPaint)
        self.namePane = wx.Panel(self)
        nameSizer = wx.BoxSizer()
        if True:
            self.nameLabel = wx.StaticText(self.namePane, label="Name")
            nameSizer.Add(self.nameLabel, 0, wx.CENTER)
        sizer.Add(self.numberBoard, 2, wx.EXPAND | wx.ALL)
        sizer.Add(self.namePane, 3, wx.LEFT | wx.RIGHT)
        self.SetSizerAndFit(sizer)
        self.SetBackgroundColour(wx.Colour(192, 192, 192))


    # Interfaces
    def refreshName(self, contestant: str):
        """
        :param contestant: name of contestant
        """
        self.nameLabel.SetLabelText(contestant)

    def getName(self):
        return self.nameLabel.GetLabelText()

    def setScore(self, score: int, violate: int):
        """
        :param score: score this constant got recently
        :param violate: times this contestant violates rule
        """
        self.scores[0] = score
        self.scores[1] = violate

    # Private Functions
    def setTextSize(self):
        size = self.namePane.GetSize()
        detectFont(size, self.nameLabel, self.getName(), ratio=0.8)
        self.namePane.SetFont(self.nameLabel.GetFont())

    def OnPaint(self, evt):
        self.setTextSize()
        dc = wx.PaintDC(self.numberBoard)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        if gc:
            size = self.numberBoard.GetSize()
            corner, SquSize = putRectangle(1.7, 1, size)
            secSize = SquSize * 0.7
            secConer = (corner[0] + SquSize, corner[1] + SquSize * 0.15)
            gc.SetBrush(wx.Brush(self.color))
            gc.DrawRectangle(*corner, SquSize, SquSize)
            gc.SetBrush(wx.Brush(wx.WHITE))
            gc.DrawRectangle(*secConer, secSize, secSize)

            s = str(self.scores[0])
            cornerN = detectFont([SquSize, SquSize], self.numberBoard, s)
            cornerN = (cornerN[0] + corner[0], cornerN[1] + corner[1])
            gc.SetFont(self.numberBoard.GetFont(), wx.WHITE)
            gc.DrawText(s, *toInts(cornerN))

            s = str(self.scores[1])
            cornerN = detectFont([secSize, secSize], self.numberBoard, s)
            cornerN = (cornerN[0] + secConer[0], cornerN[1] + secConer[1])
            gc.SetFont(self.numberBoard.GetFont(), wx.BLACK)
            gc.DrawText(s, *toInts(cornerN))

        gc.Destroy()
