import wx

from TechRecord import *
# from ViewerPanes.TechToken import *
from gcDrawer.PaintObject import *

# const
DEFAULT_INTERVAL = 5000  # 5sec


class TechBar(wx.Panel):
    """
    A timeline that shows a contestant's movements
    """
    def __init__(self, parent, isHorizonal):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        self.isH = isHorizonal
        self.beginTime = 0
        self.videoLength = 0
        self.timeInterval = DEFAULT_INTERVAL
        self.playingTime = 0
        self.techList = []

        self.childrens = []
        self.Bind(wx.EVT_PAINT, self.OnPaint, self)


    # Interfaces
    def setTimeRange(self, begin: int, interval=DEFAULT_INTERVAL):
        """
        :param begin:    the earliest time stamp where blocks can be shown
        :param interval: the time interval where blocks can be shown
        """
        self.beginTime = begin
        self.timeInterval = interval

    def setVideoLength(self, length: int):
        self.videoLength = length

    def setFromNow(self, now: int):
        """
        :param now: time playing of the video
        :return: position of slider should be
        """
        self.playingTime = now
        v = now - self.beginTime
        return max(0, min(v, self.timeInterval))

    def setFromSlider(self, value: int):
        """
        :param value: value of slider
        :return: corresponding playing time
        """
        self.playingTime = value + self.beginTime
        return self.playingTime

    def setTechList(self, techList: list[TechRecord]):
        self.techList = techList
        self.Refresh()

    def inRange(self, c: TechRecord):
        return \
            c.begin + c.interval >= self.beginTime or\
            c.begin <= self.beginTime + self.timeInterval


    # Event Catchers
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()
        # # self.DestroyChildren()
        # for c in self.childrens:
        #     c.Destroy()
        # self.childrens.clear()
        gc = wx.GraphicsContext.Create(dc)
        headY, height = self.setCorner()
        for c in self.techList:
            if not self.inRange(c):
                continue
            # args = [self, (headX, headY), (height, width), string]
            gc.SetBrush(wx.Brush(wx.Colour(225, 225, 225)))
            headX, strHeadY, width, string = self.getRecordInfo(c, height)
            if self.isH:
                gc.DrawRectangle(headX, headY, width, height)
                gc.SetFont(self.GetFont(), wx.BLACK)
                gc.DrawText(string, headX, strHeadY)
                timeX = (self.playingTime - self.beginTime) * self.GetSize().x / self.timeInterval
                gc.SetBrush(wx.Brush(wx.Colour(63, 63, 63)))
                gc.DrawRectangle(timeX, 0, 1, self.GetSize().y)
            else:
                width = self.GetSize().x * 0.95
                height = width / 5
                TechToken(None, (headY, headX), (height, width), c.atk, c.begin, c.score).draw(gc)


    # private functions
    def getRecordInfo(self, record: TechRecord, height: float):
        headX, width = self.timeTf(record)
        strHeadY, string = putPartString([width, height], self, record.atk)
        return headX, strHeadY, width, string

    def setThreeNumbers(self, record: TechRecord, width: float):
        headY = self.timeTf(record)[0]
        heights = [self.GetSize().y / 25 * c for c in (2, 3, 5)]
        strings = [toTimeFormat(record.begin), record.atk, str(record.score)]
        

    def setCorner(self):
        head = self.GetSize().y * 0.1
        height = self.GetSize().y * 0.8
        return head, height

    def timeTf(self, record: TechRecord):
        size = self.GetSize()[not self.isH]
        head = (record.begin - self.beginTime) * size / self.timeInterval
        width = record.interval * size / self.timeInterval
        return head, width

class TechToken(PaintObject):
    def __init__(self, parent, pos, size, message, time, score):
        super().__init__(parent, pos=pos, size=size)
        self.SetFont(wx.Font(16, 72, 90, 90, False, "Times New Roman"))
        tPane = PaintObject(self)
        tSizer = PaintBoxSizer(wx.VERTICAL)
        if True:
            self.timeLabel = PaintText(tPane, toTimeFormat(time))
            self.techLabel = PaintText(tPane, message)
        tSizer.Add(self.timeLabel, 2)
        tSizer.Add(self.techLabel, 3)
        self.scoreLabel = PaintText(self, str(score))
        sizer = PaintBoxSizer(wx.HORIZONTAL)
        sizer.Add(tPane, 1)
        sizer.Add(self.scoreLabel, 0)
        tPane.SetSizer(tSizer)
        self.SetSizer(sizer)

