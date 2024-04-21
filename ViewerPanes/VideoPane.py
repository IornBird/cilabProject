import wx
import wx.xrc
import wx.media

from PublicFunctions import *
from ViewerPanes.stream import *

class VideoPane(wx.Panel):
    def __init__(self, parent, streams: list[str], passTo):
        self.setPrivateMembers(passTo)
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        vidoeSizer = wx.BoxSizer(wx.VERTICAL)


        # stream
        self.stream = ShowCapture(self, streams)
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

        self.playButtom = self.playBar.AddTool(wx.ID_ANY, u"tool",
                                               wx.Bitmap(u"Images\\playButtom.png", wx.BITMAP_TYPE_ANY),
                                               wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

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

        # Connect Events
        self.Bind(wx.EVT_TOOL, self.OnPlay, self.playButtom)
        self.Bind(wx.EVT_SPINCTRL, self.OnChangeCma)
        self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnSlide, self.timeSlider)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSlideEnd, self.timeSlider)

    def __del__(self):
        pass

    def setPrivateMembers(self, passTo):
        # self.mode = (ShowCapture(self), wx.media.MediaCtrl(self))
        self.playing = False
        self.isSliding = False
        self.videos = [None, ""]  # first element must be null since it's counted from 1
        self.cameraNo = 1
        self.passLoad = passTo

    # Interfaces
    def setVideos(self, videos: list[str]):
        """
        :param videos:
        """
        self.videos = [None]
        self.videos.extend(videos)
        self.cameraNum.SetMax(len(self.videos))
        self.OnChangeCma(None)

    def getPlayingTime(self):
        """
        :return: time video playing, in milliseconds
        """
        return self.stream.getPlayingTime() #  Tell()

    def setPlayingTime(self, time: int):
        """
        :param time: time set to play from
        """
        self.stream.setTime(time)  # Seek(time)

    def getVideoLength(self):
        """
        :return: length of video in milliseconds
        """
        return self.stream.getTotalLength()  # Length()

    # Event Catcher
    def OnPlay(self, event):
        self.playing = self.stream.playing  # (self.stream.GetState() == wx.media.MEDIASTATE_PLAYING)
        self.timeSlider.SetMax(self.getVideoLength())
        if self.playing:
            self.stream.Pause()
        else:
            self.stream.Play()

    def OnChangeCma(self, event):
        self.stream.Pause()
        self.cameraNo = self.cameraNum.GetValue()
        if self.cameraNo >= len(self.videos):
            self.cameraNo = 1
        elif self.cameraNo <= 0:
            self.cameraNo = len(self.videos) - 1
        self.cameraNum.SetValue(self.cameraNo)

        # self.stream.Load(self.videos[self.cameraNo])
        self.stream.switchStream(self.cameraNo)
        if not self.playing:
            self.stream.Play()
        self.passLoad()

    def OnSlideEnd(self, evt):
        position = self.timeSlider.GetValue()
        # self.stream.Seek(position)
        self.setPlayingTime(position)
        # [self.OnPlay(None) for i in range(2)]
        self.stream.showFrame()
        self.isSliding = False

    def OnSlide(self, evt):
        self.isSliding = True

    def onTimer(self):
        if not self.isSliding:
            now = self.getPlayingTime()
            length = self.getVideoLength()
            self.timeLabel.SetLabelText(getTimeFormate(now, length))
            self.timeSlider.SetValue(now)


# m: ss.ss
def getTimeFormate(now, length):
    length -= now
    return toTimeFormat(now) + " / -" + toTimeFormat(length)
