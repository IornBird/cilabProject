import wx
import wx.xrc
import wx.media

from PublicFunctions import *
from ViewerPanes.stream import *

GUI_OBJ = None

class VideoPane(wx.Panel):
    def __init__(self, parent, streams: list[str], playbacks: list[str], fps=60):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)
        self.setPrivateMembers()

        # stream
        self.stream = GUI_OBJ  # top | ShowCapture(self, streams)

        # playing options
        self.playButton = GUI_OBJ        # self.playBar.AddTool(...)
        self.toRealTimeButton = GUI_OBJ  # self.playBar.AddTool(...)
        self.preFrameButton = GUI_OBJ    # self.playBar.AddTool(...)
        self.nxtFrameButton = GUI_OBJ    # self.playBar.AddTool(...)

        # time set
        self.timeLabel = GUI_OBJ         # bottom right | wx.StaticText(text=u"0:00.00 / -0:00.00")
        self.timeSlider = GUI_OBJ        # center       | wx.Slider
        self.cameraNum = GUI_OBJ         # wx.SpinCtrl(...)

        self.CreateControls(streams, playbacks, fps)

        # Connect Events
        # self.Bind(wx.EVT_TOOL, self.OnPlay, self.playButton)p
        self.Bind(wx.EVT_TOOL, self.OnPlayBack, self.playButton)
        self.Bind(wx.EVT_TOOL, self.stream.OnNextFrame, self.nxtFrameButton)
        self.Bind(wx.EVT_TOOL, self.stream.OnPreviousFrame, self.preFrameButton)
        self.Bind(wx.EVT_TOOL, self.stream.toRealTime, self.toRealTimeButton)

        self.Bind(wx.EVT_SPINCTRL, self.OnChangeCma)
        self.Bind(wx.EVT_SLIDER, self.OnSlide, self.timeSlider)
        # self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnSlide, self.timeSlider)
        # self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSlideEnd, self.timeSlider)

    def Destroy(self):
        self.stream.Pause()
        super().Destroy()

    def CreateControls(self, streams, playbacks, fps):
        vidoeSizer = wx.BoxSizer(wx.VERTICAL)

        # stream
        self.stream = ShowCapture(self, streams, playbacks, fps)
        # ^ wx.media.MediaCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize)
        # self.stream.Load(self.videos[1])
        # self.stream.SetPlaybackRate(1)
        # self.stream.SetVolume(1)
        # self.stream.ShowPlayerControls()
        vidoeSizer.Add(self.stream, 1, wx.ALL | wx.EXPAND, 5)

        self.timeSlider = wx.Slider(self, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL)
        vidoeSizer.Add(self.timeSlider, 0, wx.ALL | wx.EXPAND, 5)

        self.PlayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.PlayPanel.SetBackgroundColour(wx.Colour(192, 192, 192))

        playSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.playBar = wx.ToolBar(self.PlayPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.playBar.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))

        self.playButton = self.playBar.AddTool(wx.ID_ANY, u"tool",
                                               wx.Bitmap(u"Images\\playButton.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap,
                                               wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        self.toRealTimeButton = self.playBar.AddTool(wx.ID_ANY, u"tool",
                                                     wx.Bitmap(u"Images\\toRealTimeButton.png", wx.BITMAP_TYPE_ANY),
                                                     wx.NullBitmap,
                                                     wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        self.preFrameButton = self.playBar.AddTool(wx.ID_ANY, u"tool",
                                                   wx.Bitmap(u"Images\\preFrameButton.png", wx.BITMAP_TYPE_ANY),
                                                   wx.NullBitmap,
                                                   wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        self.nxtFrameButton = self.playBar.AddTool(wx.ID_ANY, u"tool",
                                                   wx.Bitmap(u"Images\\nxtFrameButton.png", wx.BITMAP_TYPE_ANY),
                                                   wx.NullBitmap,
                                                   wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.playBar.SetBackgroundColour(self.PlayPanel.GetBackgroundColour())

        self.playBar.Realize()

        playSizer.Add(self.playBar, 0, wx.EXPAND, 5)

        self.timeLabel = wx.StaticText(self.PlayPanel, wx.ID_ANY, u"0:00.00 / -0:00.00", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.timeLabel.Wrap(-1)
        self.timeLabel.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Consolas"))

        playSizer.Add(self.timeLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        self.cameraSet = wx.Panel(self.PlayPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        cameraSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.cameraText = wx.StaticText(self.cameraSet, wx.ID_ANY, u"Camera", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cameraText.Wrap(-1)
        cameraSizer.Add(self.cameraText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cameraNum = wx.SpinCtrl(self.cameraSet, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.SP_ARROW_KEYS
                                     , 0, len(self.videos), 1)
        cameraSizer.Add(self.cameraNum, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cameraSet.SetSizer(cameraSizer)
        self.cameraSet.Layout()
        cameraSizer.Fit(self.cameraSet)
        playSizer.Add(self.cameraSet, 1, wx.EXPAND | wx.ALL, 0)

        self.PlayPanel.SetSizer(playSizer)
        self.PlayPanel.Layout()
        playSizer.Fit(self.PlayPanel)
        vidoeSizer.Add(self.PlayPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(vidoeSizer)
        self.Layout()

    def setPrivateMembers(self):
        # self.mode = (ShowCapture(self), wx.media.MediaCtrl(self))
        self.streaming = True
        self.playing = False
        self.isSliding = False
        self.videos = [None, ""]  # first element must be null since it's counted from 1
        self.cameras = [None, ""]
        self.cameraNo = 1
        self.modified = False
        # self.passLoad = passTo

    # Interfaces
    def setVideos(self, videos: list[str]):
        """
        set ALL video that will be switch to
        :param videos:
        """
        self.videos = [None]
        self.videos.extend(videos)

        self.cameraNum.SetMax(len(self.videos))
        self.OnChangeCma(None)

    def getPlayingTime(self):
        """
        :return: time video playing, in milliseconds.
            if time isn't modified by slider, returns reversed of that.
        """
        ans = self.stream.getPlayingTime()  # Tell()
        if self.modified:
            return ans
        return ~ans

    def setPlayingTime(self, time: int):
        """
        :param time: time set to play from
        """
        self.modified = (time >= 0)
        if self.modified:
            self.stream.setTime(time)
        self.onTimer()
        # wx.CallAfter(self.stream.setTime, time)  # Seek(time)
        # wx.CallAfter(self.onTimer)

    def getVideoLength(self):
        """
        :return: length of video in milliseconds
        """
        return self.stream.getTotalLength()  # Length()

    def GameRun(self, pause: bool):
        if pause:
            self.stream.GamePause()
        else:
            self.stream.GamePlay()

    # Event Catcher
    def OnPlay(self, event):
        timeTag("VideoPane::OnPlay")
        self.playing = self.stream.playing  # (self.stream.GetState() == wx.media.MEDIASTATE_PLAYING)
        self.timeSlider.SetMax(self.getVideoLength())
        if self.playing:
            self.stream.Pause()
        else:
            self.stream.Play()

    def OnPlayBack(self, evt):
        self.stream.toPlayBack()
        if self.playing:
            self.stream.Pause()
        else:
            self.stream.Play()

    def OnRealTime(self, evt):
        self.stream.toRealTime(evt)

    def OnChangeCma(self, event):
        self.stream.Pause()
        self.cameraNo = self.cameraNum.GetValue()
        if self.cameraNo >= len(self.videos):
            self.cameraNo = 1
        elif self.cameraNo <= 0:
            self.cameraNo = len(self.videos) - 1
        self.cameraNum.SetValue(self.cameraNo)

        # self.stream.Load(self.videos[self.cameraNo])
        self.stream.switchStream(self.cameraNo - 1)
        if self.playing:
            self.stream.Play()
        # self.passLoad()  # <-HERE

    def OnSlideEnd(self, evt):
        pass

    def OnSlide(self, evt):
        self.modified = True
        if self.isSliding:
            return
        self.isSliding = True
        position = self.timeSlider.GetValue()
        # self.stream.Seek(position)
        self.setPlayingTime(position)
        # [self.OnPlay(None) for i in range(2)]
        self.stream.showFrame()
        self.isSliding = False

    def onTimer(self):
        # if not self.isSliding:
        self.stream.OnWxTimer(self.modified)
        now = self.getPlayingTime()
        length = self.getVideoLength()
        if now < 0: now = ~now
        self.timeLabel.SetLabelText(getTimeFormate(now, length))
        self.timeSlider.SetMax(length)
        self.timeSlider.SetValue(now)
        self.modified = False


# m: ss.ss
def getTimeFormate(now, length):
    length -= now
    return toTimeFormat(now) + " / -" + toTimeFormat(length)
