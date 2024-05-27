import wx
from PublicFunctions import *


class ScorePane(wx.Panel):
    """
    A panel that shows score and times of violating rules of a contestant
    """
    def __init__(self, parent, isBlue, scores):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        self.SetFont(wx.Font(36, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.color = wx.BLUE if isBlue else wx.RED
        self.scores = scores
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.numberBoard = wx.Panel(self, style=wx.TRANSPARENT_WINDOW)
        if True:
            self.numberBoard.SetBackgroundStyle(wx.BG_STYLE_PAINT)
            self.numberBoard.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.nameLabel = "Name"
        self.namePane = wx.Panel(self, size=self.GetTextExtent("Name"), style=wx.TRANSPARENT_WINDOW)
        # nameSizer = wx.BoxSizer()
        # if True:
        #     self.nameLabel = wx.StaticText(self.namePane, label="Name")
        #     nameSizer.Add(self.nameLabel, 1, wx.EXPAND | wx.CENTER)
        sizer.Add(self.numberBoard, 2, wx.EXPAND | wx.ALL)
        sizer.Add(self.namePane, 3, wx.EXPAND | wx.LEFT | wx.RIGHT)
        self.SetSizerAndFit(sizer)
        self.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.needRefersh = False


    # Interfaces
    def refreshName(self, contestant: str):
        """
        :param contestant: name of contestant
        if containing last name, only first letter of which will be shown
        """
        name = contestant.split(' ')
        self.nameLabel = name[-1]
        if len(name) > 1:
            self.nameLabel += f" {name[0][0]}."
        self.Refresh()

    def getName(self):
        return self.nameLabel

    def setScore(self, score: int, violate: int):
        """
        :param score: score this constant got recently
        :param violate: times this contestant violates rule
        """
        self.scores[0] = score
        self.scores[1] = violate
        self.Refresh()

    # Private Functions
    def setTextSize(self, gc: wx.GraphicsContext):
        size = self.namePane.GetSize()
        tf = wx.AffineMatrix2D()
        # gct = wx.GraphicsContext.Create(dc)
        gc.SetFont(self.GetFont(), wx.BLACK)
        tSize = self.GetTextExtent(self.nameLabel)

        t_size_copy = [*tSize]
        corner_copy = [0, 0]

        c, times = putRectangle(tSize[0], tSize[1], size, 0.8)
        tf.Translate(c[0] + self.numberBoard.GetSize()[0], c[1])
        tf.Scale(times, times)
        gc.SetTransform(gc.CreateMatrix(tf))

        t_size_copy = tf.TransformPoint(t_size_copy)
        corner_copy = tf.TransformPoint(corner_copy)

        print("from: ", *corner_copy)
        print("to:   ", *t_size_copy)

        gc.DrawText(self.nameLabel, 0, 0)
        del tf
        # detectFont(size, self.nameLabel, self.getName(), ratio=0.8)
        # self.namePane.SetFont(self.nameLabel.GetFont())
        # gct.Destroy()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
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
            self.setTextSize(gc)

        gc.Destroy()
        self.RefershAgain()

    def RefershAgain(self):
        if self.needRefersh:
            self.Refresh()
            self.Update()
        self.needRefersh = not self.needRefersh
