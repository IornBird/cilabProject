import wx
from ViewerPanes.ScorePane import ScorePane
from ViewerPanes.TechBar import TechBar
from TechRecord import TechRecord

class ScoreBar(wx.Panel):
    def __init__(self, parent, record):
        super().__init__(parent)

        self.scroll = None         # top    of all | wx.ScrollBar(self, style=wx.SB_HORIZONTAL)

        self.BlueScore = None      # left  top     | ScorePane(self, True)
        self.BlueList = None       # right top     | TechBar(self)
        self.RedScore = None       # left  bottom  | ScorePane(self, False)
        self.RedList = None        # right bottom  | TechBar(self)

        self.timeSpecifier = None  # bottom of all | wx.Slider(self)

        self.record = record
        self.playingTime = 0
        self.videoLength = 0

        self.modified = False

        Lst = [(c // 2 + 1, c % 2) for c in range(4)]
        SclPlc = [(3, 0), (1, 2)]
        self.CreateControls(Lst, SclPlc)

        self.Bind(wx.EVT_PAINT, self.OnPaint, self)
        self.Bind(wx.EVT_SCROLL, self.OnScroll, self.scroll)

        self.sliding = False
        self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnSlideBegin, self.timeSpecifier)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSlideEnd, self.timeSpecifier)

    def CreateControls(self, Lst, SclPlc):
        self.sizer = wx.GridBagSizer(1, 1)
        if True:
            self.BlueScore = ScorePane(self, True)
            self.BlueList = TechBar(self)
            self.RedScore = ScorePane(self, False)
            self.RedList = TechBar(self)
            self.scroll = wx.ScrollBar(self, style=wx.SB_HORIZONTAL)

        self.timeSpecifier = wx.Slider(self)
        self.sizer.Add(self.timeSpecifier, (0, 1), (1, 1), wx.EXPAND | wx.ALL)

        self.sizer.Add(self.BlueScore, Lst[0], (1, 1), wx.CENTER | wx.EXPAND | wx.ALL)
        self.sizer.Add(self.BlueList, Lst[1], (1, 1), wx.EXPAND | wx.ALL)
        self.sizer.Add(self.RedScore, Lst[2], (1, 1), wx.CENTER | wx.EXPAND | wx.ALL)
        self.sizer.Add(self.RedList, Lst[3], (1, 1), wx.EXPAND | wx.ALL)
        self.sizer.Add(self.scroll, SclPlc[0], SclPlc[1], wx.EXPAND | wx.ALL)
        self.SetSizerAndFit(self.sizer)

        self.sizer.AddGrowableRow(1)
        self.sizer.AddGrowableRow(2)
        self.sizer.AddGrowableCol(1)

        self.sizer.SetMinSize(50, 50)
        self.SetSizerAndFit(self.sizer)

    # Interfaces
    def setTechRecord(self, records: tuple):
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
            self.render()

            # self.Refresh()

    def getSetTime(self):
        """
        :return: time user set on this pane, -1 if user didn't set.
        """
        if self.modified:
            return self.playingTime
        return -1


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
        showRange = self.BlueList.timeInterval
        self.timeSpecifier.SetRange(0, showRange)

    def findTechFrom(self, time: int):
        """
        :param time: length of video in milliseconds
        :return : [tech on blue, tech on red], None if not found
        """

    # Event Catchers
    def OnScroll(self, evt):
        val = self.scroll.GetThumbPosition()
        self.RedList.setTimeRange(val)
        self.BlueList.setTimeRange(val)

        self.modified = True
        self.Refresh()

    def OnTimer(self):
        self.modified = False

    def OnSlideBegin(self, evt):
        self.modified = True
        self.sliding = True

    def OnSlideEnd(self, evt):
        v = self.timeSpecifier.GetValue()
        now = self.BlueList.setFromSlider(v)
        self.RedList.setFromSlider(v)
        self.setPlayingTime(now)
        self.sliding = False

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()
        # self.render(dc)

    # Private Functions
    def render(self):
        self.RedList.setTechList(self.record[0][1])
        self.BlueList.setTechList(self.record[1][1])
        if not self.sliding:
            self.timeSpecifier.SetValue(self.getSliderValue())

    def getSliderValue(self):
        self.RedList.setFromNow(self.playingTime)
        return self.BlueList.setFromNow(self.playingTime)
