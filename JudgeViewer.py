import threading
import time

import wx

from PublicFunctions import AnyTypeToInts
from ViewerPanes.ScoreSet import ScoreSetPane
from ViewerPanes.ScoreBar import ScoreBar
from ViewerPanes.VideoPane import VideoPane
from TechRecord import TechRecord, Tech

from TimeManager import TimeManager

import SQL.mysql_api as sql

# demo
# IPs = ['192.168.100.127', '192.168.100.108']
# playbacks = [
#             #"C:\\Users\\User\\Desktop\\source\\桂格超大便當.mp4",
#             #"E:\\專題\\test.mp4",
#             "videos/0.avi",
#             "C:\\Users\\User\\Desktop\\source\\source2\\Miyabi_Love_You.mp4"
#         ]
#
# f = open("./videos/0.avi", 'rb')
# f.close()
#
# techRecord = (
#             ["Yume", [TechRecord(0, Tech.KICK, Tech.TRUNK), TechRecord(2000, Tech.PUNCH, Tech.HEAD)]],
#             ["Laura", [TechRecord(500, Tech.T_KICK, Tech.HEAD)]]
#         )
# judgeScores = ([0, 0], [0, 0])

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

import Streamers.SharedData as SD

FPS = 60

class JudgeViewer(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.timer = wx.Timer(self)

        self.timePlaying = 0
        self.gamePaused = True  # True iff timer of contest itself is paused
        self.TechRecord = SD.techRecord  # format is ([blue name, blue record], [red name, red record])
        self.Scores = SD.judgeScores     # formate is ([blue score, blue violates], [red score, red violates])

        self.scoreSet = None   # left top  | ScoreSetPane(vtSpliter, None, None)
        self.videoPane = None  # right top | VideoPane(vtSpliter, IPs, self.needReload)
        self.timeLine = None   # bottom    | ScoreBar(hrSpliter, wx.HORIZONTAL, self.passTime)

        self.CreateControls()
        self.timer.Start(round(1000 / FPS))

        self.doTimeSet = False
        self.videoNotLoad = True

        self.timerProcessing = False

    def CreateControls(self):
        sizer = wx.BoxSizer()
        hrSpliter = wx.SplitterWindow(self, style=wx.SP_BORDER | wx.SP_LIVE_UPDATE)
        if True:  # set detail for hrSpliter
            vtSpliter = wx.SplitterWindow(hrSpliter, style=wx.SP_BORDER | wx.SP_LIVE_UPDATE)
            if True:  # set detail for vtSpliter
                self.scoreSet = ScoreSetPane(vtSpliter, self.TechRecord, self.Scores)
                self.videoPane = VideoPane(vtSpliter, SD.IPs, SD.playbacks, FPS)
            vtSpliter.SetSashGravity(0.4)
            vtSpliter.SplitVertically(self.scoreSet, self.videoPane)
            self.timeLine = ScoreBar(hrSpliter, self.TechRecord, self.Scores)
        hrSpliter.SetSashGravity(0.7)
        hrSpliter.SplitHorizontally(vtSpliter, self.timeLine)
        sizer.Add(hrSpliter, 1, wx.EXPAND | wx.ALL)
        self.SetSizerAndFit(sizer)

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        # self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyEvent)
        self.SetFocus()
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    # Interfaces
    def addRecord(self, isBlue, record):
        self.TechRecord[not isBlue].append(record)

    def setRecord(self, t: tuple):
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

    def updateTimeline(self):
        self.timeLine.OnScoreSet()

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

        vidNow = self.videoPane.getPlayingTime()  # less than 0 means it's not modified
        tLineNow = self.timeLine.getSetTime()
        modifySS = False
        if tLineNow != -1:
            self.timePlaying = tLineNow
            modifySS = True
        else:
            if vidNow < 0:
                vidNow = ~vidNow
            else:
                modifySS = True
            self.timePlaying = vidNow
        self.videoPane.setPlayingTime(tLineNow)
        self.timeLine.OnTimer(self.timePlaying)

        self.timeLine.setVideoLength(self.videoPane.getVideoLength())

        # self.timePlaying = vidNow
        self.scoreSet.setTime(self.timePlaying, modifySS)
        # self.Refresh()
        # for c in (
        #     (self.videoPane.setPlayingTime, self.timePlaying),
        #     (self.timeLine.setPlayingTime, self.timePlaying),
        #     (self.scoreSet.findTech, self.timePlaying)
        # ):
        #     threading.Thread(target=c[0], args=(c[1],)).start()
        #
        # end = threading.Thread(target=wx.CallAfter, args=(self.Refresh,))
        # end.start()
        # end.join()

        # # TODO: get data from core

        # now = time.time() - now
        # print(now, "second passed")

        self.timerProcessing = False

    def OnKeyEvent(self, evt):
        # assert isinstance(evt, wx.KeyEvent)
        # code = evt.GetKeyCode()
        # if code == 32:
        # self.gamePaused = not self.gamePaused
        self.videoPane.GameRun()
        # elif code == 0:
        #     raise KeyError("Set keyboard to English(US)")
        # else:
        #     evt.Skip()

    def OnImport(self, evt):
        with open("INFO\\Contestants.txt", 'rt') as f:
            L = f.read().split('\n')
            blue = L[0][3:]
            red = L[1][3:]
        self.TechRecord[0][0] = blue
        self.TechRecord[1][0] = red
        hasRed = sql.select_db('contestant', 'id', f"name='{red}'")
        if not hasRed:
            sql.insert_db("contestant", (1001, red, 'unknown'))
        hasBlue = sql.select_db('contestant', 'id', f"name='{blue}'")
        if not hasBlue:
            sql.insert_db("contestant", (1002, blue, 'unknown'))
        self.timeLine.refreshNames()
        self.Reset()

    def OnFlush(self, evt):
        print("OnFlush")
        blueID = sql.select_db('contestant', 'id', f"name='{self.TechRecord[0][0]}'")[0][0]
        redID = sql.select_db('contestant', 'id', f"name='{self.TechRecord[1][0]}'")[0][0]
        with open("INFO\\Contest Place.txt") as f:
            d = {}
            L = f.read().split('\n')
            for c in L:
                p = c.split(':_')
                d[p[0]] = p[1]
        redScore = self.Scores[1][0]
        blueScore = self.Scores[0][0]
        if redScore > blueScore:
          winner = redID
        elif redScore > blueScore:
          winner = blueID
        else: winner = -1  # draw

        args = ('1001',
                 d['name'], d['date'], d['location'], d['log'],
                 redID, blueID, winner, self.Scores[1][0], self.Scores[0][0])
        sql.insert_db('competition', args)
        self.Reset()

    def Reset(self):
        for i in range(4):
            self.Scores[i // 2][i % 2] = 0
        # self.TechRecord  # format is ([blue name, blue record], [red name, red record])
        self.TechRecord[0][1].clear()
        self.TechRecord[1][1].clear()

        self.setTechRecord()


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
        [self.videoPane.OnPlaySwitch(None) for i in range(2)]  # get the frame now

    # Private Function
    def setTechRecord(self):
        self.timeLine.setTechRecord(self.TechRecord)

    # Destructor
    def Destroy(self):
        self.timer.Stop()
        super().Destroy()

