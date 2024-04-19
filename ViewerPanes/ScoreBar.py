import wx
from ViewerPanes.ScorePane import ScorePane
from ViewerPanes.TechBar import TechBar
from TechRecord import TechRecord

class ScoreBar(wx.Panel):
    def __init__(self, parent, style, passTo):
        super().__init__(parent)

        self.isH = False
        self.record = [("name1", []), ("name2", [])]
        self.playingTime = 0
        self.videoLength = 0
        self.passTime = passTo

        if style == wx.HORIZONTAL:
            Lst = [(c // 2 + 1, c % 2) for c in range(4)]
            SclPlc = [(3, 0), (1, 2)]
            self.isH = True
        elif style == wx.VERTICAL:
            Lst = [(c % 2, c // 2) for c in range(4)]
            SclPlc = [(0, 2), (2, 1)]
            self.isH = False
        else:
            raise ValueError("Please specify the arrangement.")
        self.CreateControls(Lst, SclPlc)
        self.Bind(wx.EVT_PAINT, self.OnPaint, self)
        self.Bind(wx.EVT_SCROLL, self.OnScroll, self.scroll)
        if self.isH:
            self.sliding = False
            self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnSlideBegin, self.timeSpecifier)
            self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSlideEnd, self.timeSpecifier)

    def CreateControls(self, Lst, SclPlc):
        self.sizer = wx.GridBagSizer(1, 1)
        if True:
            self.BlueScore = ScorePane(self, True)
            self.BlueList = TechBar(self, self.isH)
            self.RedScore = ScorePane(self, False)
            self.RedList = TechBar(self, self.isH)
            self.scroll = wx.ScrollBar(self, style=
                wx.SB_HORIZONTAL if self.isH else wx.SB_VERTICAL)
        if self.isH:
            self.timeSpecifier = wx.Slider(self)
            self.sizer.Add(self.timeSpecifier, (0, 1), (1, 1), wx.EXPAND | wx.ALL)
        self.sizer.Add(self.BlueScore, Lst[0], (1, 1), wx.CENTER | wx.EXPAND | wx.ALL)
        self.sizer.Add(self.BlueList, Lst[1], (1, 1), wx.EXPAND | wx.ALL)
        self.sizer.Add(self.RedScore, Lst[2], (1, 1), wx.CENTER | wx.EXPAND | wx.ALL)
        self.sizer.Add(self.RedList, Lst[3], (1, 1), wx.EXPAND | wx.ALL)
        self.sizer.Add(self.scroll, SclPlc[0], SclPlc[1], wx.EXPAND | wx.ALL)
        self.SetSizerAndFit(self.sizer)

        if self.isH:
            self.sizer.AddGrowableRow(1)
            self.sizer.AddGrowableRow(2)
            self.sizer.AddGrowableCol(1)
        else:
            self.sizer.AddGrowableCol(0)
            self.sizer.AddGrowableCol(1)
            self.sizer.AddGrowableRow(1)
        self.sizer.SetMinSize(50, 50)
        self.SetSizerAndFit(self.sizer)

    # Interfaces
    def setTechRecord(self, records: tuple[str, list[TechRecord]]):
        """
        :param records: movements of both contestant
               format is ([name1, record1], [name2, record2])
        """
        self.record = records
        self.RedScore.SetName(records[0][0])
        self.BlueScore.SetName(records[1][0])

    def setPlayingTime(self, time: int):
        """
        :param time: in milliseconds since the video begins
        """
        if self.playingTime != time:
            self.playingTime = time
            self.Refresh()

    def setVideoLength(self, time: int):
        """
        :param time: length of video in milliseconds
        """
        self.videoLength = time
        self.scroll.SetScrollbar(
            self.scroll.GetThumbPosition(),
            self.scroll.GetThumbSize(),
            time,
            self.scroll.GetPageSize()
        )
        if self.isH:
            showRange = self.BlueList.timeInterval
            self.timeSpecifier.SetRange(0, showRange)


    # Event Catchers
    def OnScroll(self, evt):
        val = self.scroll.GetThumbPosition()
        self.RedList.setTimeRange(val)
        self.BlueList.setTimeRange(val)
        self.Refresh()

    def OnTimer(self):
        pass

    def OnSlideBegin(self, evt):
        self.sliding = True

    def OnSlideEnd(self, evt):
        v = self.timeSpecifier.GetValue()
        now = self.BlueList.setFromSlider(v)
        self.RedList.setFromSlider(v)
        self.setPlayingTime(now)
        self.passTime(now)
        self.sliding = False

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()
        self.render(dc)

    # Private Functions
    def render(self, dc):
        self.RedList.setTechList(self.record[0][1])
        self.BlueList.setTechList(self.record[1][1])
        if self.isH and not self.sliding:
            self.timeSpecifier.SetValue(self.getSliderValue())

    def getSliderValue(self):
        self.RedList.setFromNow(self.playingTime)
        return self.BlueList.setFromNow(self.playingTime)
