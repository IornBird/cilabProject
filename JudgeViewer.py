import threading
import time

import wx
from ViewerPanes.ScoreSet import ScoreSetPane
from ViewerPanes.ScoreBar import ScoreBar
from ViewerPanes.VideoPane import VideoPane
from TechRecord import TechRecord, Tech

import SQL.mysql_api as sql

# demo
IPs = ['192.168.100.127', '192.168.100.108']
playbacks = []

techRecord = (
            ["Yume", [TechRecord(0, Tech.KICK, Tech.TRUNK, 2), TechRecord(2000, Tech.PUNCH, Tech.HEAD, 0)]],
            ["Laura", [TechRecord(500, Tech.T_KICK, Tech.HEAD, 3)]]
        )

"""
custom event
myEVT_CUSTOM = wx.NewEventType()
EVT_CUSTOM = wx.PyEventBinder(myEVT_CUSTOM, 1)

class MyEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        myVal = None

    def SetMyVal(self, val):
        self.myVal = val

    def GetMyVal(self):
        return self.myVal
"""

FPS = 60
now = time.time()

class JudgeViewer(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.timer = wx.Timer(self)

        self.timePlaying = 0
        self.gamePaused = False  # True iff timer of contest itself is paused
        self.TechRecord = techRecord #(["", []], ["", []])  # format is ([blue name, blue record], [red name, red record])
        self.Scores = ([0, 0], [0, 0])  # formate is ([blue score, blue violates], [red score, red violates])

        self.scoreSet = None   # left top  | ScoreSetPane(vtSpliter, None, None)
        self.videoPane = None  # right top | VideoPane(vtSpliter, IPs, self.needReload)
        self.timeLine = None   # bottom    | ScoreBar(hrSpliter, wx.HORIZONTAL, self.passTime)

        self.CreateControls()
        self.timer.Start(round(1000 / FPS))

        self.doTimeSet = False
        self.videoNotLoad = True

        self.timerProcessing = False
        # demo
        self.loadVideos(IPs)

        # self.loadVideos([
        #     "C:\\Users\\User\\Downloads\\explaning.mp4",
        #     "C:\\Users\\User\\Desktop\\source\\桂格超大便當.mp4",
        #     "C:\\Users\\User\\Desktop\\source\\source2\\Miyabi_Love_You.mp4"
        # ])

    def CreateControls(self):
        sizer = wx.BoxSizer()
        hrSpliter = wx.SplitterWindow(self, style=wx.SP_BORDER | wx.SP_LIVE_UPDATE)
        if True:  # set detail for hrSpliter
            vtSpliter = wx.SplitterWindow(hrSpliter, style=wx.SP_BORDER | wx.SP_LIVE_UPDATE)
            if True:  # set detail for vtSpliter
                self.scoreSet = ScoreSetPane(vtSpliter, None, None)
                self.videoPane = VideoPane(vtSpliter, IPs, self.needReload)
            vtSpliter.SetSashGravity(0.4)
            vtSpliter.SplitVertically(self.scoreSet, self.videoPane)
            self.timeLine = ScoreBar(hrSpliter, self.TechRecord)
        hrSpliter.SetSashGravity(0.7)
        hrSpliter.SplitHorizontally(vtSpliter, self.timeLine)
        sizer.Add(hrSpliter, 1, wx.EXPAND | wx.ALL)
        self.SetSizerAndFit(sizer)

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvent)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    # Interfaces
    def setRecord(self, tuple):
        pass

    def loadVideos(self, videos: list[str]):
        """
        :param videos: paths of videos
        """
        self.videoPane.setVideos(videos)
        self.videoNotLoad = self.needReload()

    def pause(self):
        self.gamePaused = True

    def resume(self):
        self.gamePaused = False

    # Event Catcher
    def OnTimer(self, evt):
        """
        read: (any time)
            time from self.videoPane
            time from self.timeLine, if it's rewritten
            change from self.scoreSet
        write:
            time of self
            time of self.videoPane
            time of self.timeLine
            record of self.scoreSet, by time
        """
        if self.timerProcessing:
            return
        self.timerProcessing = True

        # global now
        # now = time.time() - now
        # print(now, "second passed since last call")

        vidNow = self.videoPane.getPlayingTime()
        tLineNow = self.timeLine.getSetTime()
        if tLineNow != -1:
            vidNow = tLineNow
        self.timePlaying = vidNow
        for c in (
            (self.videoPane.setPlayingTime, self.timePlaying),
            (self.timeLine.setPlayingTime, self.timePlaying),
            (self.scoreSet.findTech, self.timePlaying)
        ):
            threading.Thread(target=c[0], args=(c[1],)).start()

        end = threading.Thread(target=wx.CallAfter, args=(self.Refresh,))
        end.start()
        end.join()

        # # TODO: get data from core

        # now = time.time() - now
        # print(now, "second passed")

        self.timerProcessing = False

    def OnKeyEvent(self, evt):
        assert isinstance(evt, wx.KeyEvent)
        code = evt.GetKeyCode()
        if code == 32:
            self.gamePaused = not self.gamePaused
        elif code == 0:
            raise KeyError("Set keyboard to English(US)")

    def OnDetected(self, evt):
        pass

    def needReload(self):
        length = self.videoPane.getVideoLength()
        self.videoNotLoad = (length == 0)
        if self.videoNotLoad:
            return True
        self.timeLine.setVideoLength(length)
        return False

    def passTime(self, time: int):
        """
        :param time: time set to video
        """
        self.videoPane.setPlayingTime(time)
        [self.videoPane.OnPlay(None) for i in range(2)]  # get the frame now

    # Private Function
    def setTechRecord(self):
        self.timeLine.setTechRecord(self.TechRecord)

    # Destructor
    def Destroy(self):
        self.timer.Stop()
        super().Destroy()

