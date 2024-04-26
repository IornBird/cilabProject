import threading

import wx

from TechRecord import *
# from ViewerPanes.TechToken import *
# from gcDrawer.PaintObject import *

# const
DEFAULT_INTERVAL = 5000  # 5sec
DEFAULT_SHOW = 1000 # 1sec


class TechBar(wx.Panel):
    """
    A timeline that shows a contestant's movements
    """
    def __init__(self, parent):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        self.isH = True
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
            c.time + DEFAULT_SHOW >= self.beginTime or\
            c.time <= self.beginTime + self.timeInterval

    # Event Catchers
    def OnPaint(self, evt):
        """
        put:
        v
        +-----+ <- 0.1 * height
        |  0  | <- 0.8 of height
        +-----+ <- height = 0.9 * height
          ^ width = width * timeItv / showItv
        on self

        get size of rectangle
        get times needs for text
        """
        dc = wx.PaintDC(self)
        dc.Clear()

        gc = wx.GraphicsContext.Create(dc)
        gct = wx.GraphicsContext.Create(dc)

        th = threading.Thread(target=self.threadRender, args=(gc, gct))
        th.start()
        # self.threadRender(gc, gct)

    # private functions
    def setRectSize(self):
        pass

    def threadRender(self, gc, gct):
        cornerY, height = self.setCornerY()
        cornerX, width = self.timeTf(0)

        strSize = self.GetTextExtent("0")
        strCorner, strTimes = putRectangle(*strSize, [width, height])
        font = self.GetFont().Scaled(strTimes)
        self.SetFont(font)
        tf = wx.AffineMatrix2D()

        tf.Translate(*strCorner)
        # tf.Scale(strTimes, strTimes)
        gct.SetTransform(gct.CreateMatrix(tf))
        gct.SetFont(self.GetFont(), wx.BLACK)

        gc.SetBrush(wx.Brush(wx.Colour(225, 225, 225)))

        for c in self.techList:
            if not self.inRange(c):
                continue
            cornerX, width = self.timeTf(c.time)
            wx.CallAfter(lambda: [
                gc.DrawRectangle(cornerX, cornerY, width, height),
                gct.DrawText(str(c.score), cornerX, 0)
            ])

        timeX = (self.playingTime - self.beginTime) * self.GetSize().x / self.timeInterval
        wx.CallAfter(lambda: [
            gc.SetBrush(wx.Brush(wx.Colour(63, 63, 63))),
            gc.DrawRectangle(timeX, 0, 1, self.GetSize().y)
        ])


    '''
    def getRecordInfo(self, record: TechRecord, height: float):
        headX, width = self.timeTf(record)
        strHeadY, string = putPartString([width, height], self, record.atk)
        return headX, strHeadY, width, string

    def setThreeNumbers(self, record: TechRecord, width: float):
        headY = self.timeTf(record)[0]
        heights = [self.GetSize().y / 25 * c for c in (2, 3, 5)]
        strings = [toTimeFormat(record.begin), record.atk, str(record.score)]
    '''

    def setCornerY(self):
        head = self.GetSize().y * 0.1
        height = self.GetSize().y * 0.8
        return head, height

    def timeTf(self, begin: int, interval=DEFAULT_SHOW):
        size = self.GetSize()[not self.isH]
        head = (begin - self.beginTime) * size / self.timeInterval
        width = interval * size / self.timeInterval
        return head, width

'''
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
'''
