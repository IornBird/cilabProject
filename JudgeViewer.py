import wx
from ViewerPanes.ScoreBar import ScoreBar
from ViewerPanes.VideoPane import VideoPane
from TechRecord import TechRecord

import SQL.mysql_api as sql

class JudgeViewer(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.CreateControls()
        self.videoNotLoad = True
        self.timer.Start(30)
        # demo
        self.loadVideos([
            "C:\\Users\\User\\Downloads\\explaning.mp4",
            "C:\\Users\\User\\Desktop\\source\\桂格超大便當.mp4",
            "C:\\Users\\User\\Desktop\\source\\source2\\Miyabi_Love_You.mp4"
        ])
        self.setTechRecord((
            ["Yume", [TechRecord(0, 1000, "A1", 0), TechRecord(2000, 3000, "A2", 0)]],
            ["Laura", [TechRecord(500, 1500, "A3", 0), TechRecord(2000, 2500, "A4", 0)]]
        ))

    def CreateControls(self):
        self.timer = wx.Timer(self)
        sizer = wx.BoxSizer()
        hrSpliter = wx.SplitterWindow(self, style=wx.SP_BORDER | wx.SP_LIVE_UPDATE)
        if True:  # set detail for hrSpliter
            vtSpliter = wx.SplitterWindow(hrSpliter, style=wx.SP_BORDER | wx.SP_LIVE_UPDATE)
            if True:  # set detail for vtSpliter
                self.techList = ScoreBar(vtSpliter, wx.VERTICAL, self.passTime)
                self.videoPane = VideoPane(vtSpliter, self.needReload)
            vtSpliter.SetSashGravity(0.4)
            vtSpliter.SplitVertically(self.techList, self.videoPane)
            self.timeLine = ScoreBar(hrSpliter, wx.HORIZONTAL, self.passTime)
        hrSpliter.SetSashGravity(0.7)
        hrSpliter.SplitHorizontally(vtSpliter, self.timeLine)
        sizer.Add(hrSpliter, 1, wx.EXPAND | wx.ALL)
        self.SetSizerAndFit(sizer)

        self.Bind(wx.EVT_TIMER, self.OnTimer)

    # Interfaces
    def setTechRecord(self, records: tuple[str, list[TechRecord]]):
        self.techList.setTechRecord(records)
        self.timeLine.setTechRecord(records)

    def loadVideos(self, videos: list[str]):
        """
        :param videos: paths of videos
        """
        self.videoPane.setVideos(videos)
        self.videoNotLoad = self.needReload()

    # Event Catcher
    def OnTimer(self, evt):
        now = self.videoPane.getPlayingTime()
        self.videoPane.onTimer()
        # TODO: get data from core
        if self.videoNotLoad:
            self.needReload()
        self.timeLine.setPlayingTime(now)
        self.techList.setPlayingTime(now)

    def needReload(self):
        length = self.videoPane.getVideoLength()
        self.videoNotLoad = (length == 0)
        if self.videoNotLoad:
            return True
        self.timeLine.setVideoLength(length)
        self.techList.setVideoLength(length)
        return False

    def passTime(self, time: int):
        """
        :param time: time set to video
        """
        self.videoPane.setPlayingTime(time)
        [self.videoPane.OnPlay(None) for i in range(2)]  # get the frame now

    # Destructor
    def Destroy(self):
        self.timer.Stop()
        super().Destroy()

