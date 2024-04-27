import cv2
import wx
import time
from PublicFunctions import timeTag
from TimeManager import TimeManager

class StreamPlayer:
    """
    stream player that can be playback
    this class will be used by some subclass of wx.Panel
    """
    def __init__(self, streams: list[cv2.VideoCapture], fps=60):
        self.cameras = streams
        self.camera_no = 0
        self.timePlaying = 0  # 0 means begin of the stream
        self.realTime = 0
        self.fps = fps
        self.frameLen = round(1000 / fps)
        self.PlManager = TimeManager()
        self.RTManager = TimeManager()

    def chooseStream(self, n: int):
        """
        play n-th stream, either in real time or playback
        """
        if not (0 <= n < len(self.cameras)):
            raise ValueError("Chosen stream does not exist")
        self.camera_no = n

    def setTime(self, past_ms: int):
        """
        play current stream from past_ms before real-time
        :param past_ms: time (in ms) before real-time to be played from
        """
        self.timePlaying = self.realTime - past_ms
        self.PlManager.SetTime(self.timePlaying)

    def getFrame(self):
        """
        get the frame in current stream at self.timePlaying
        It's called only when the player is playing
        :returns : the frame in current stream
        """
        timeTag("StreamPlayer::getFrame")
        self.cameras[self.camera_no].set(cv2.CAP_PROP_POS_MSEC, self.timePlaying)
        ret, frame = self.cameras[self.camera_no].read()
        timeTag("[return]")
        return frame

    def viewNextNFrame(self, n: int):
        """
        show the n-th frame if the frame at self.timePlaying is 0-th
        n can be negative, like -1 means previous frame
        It's called only when the player is gamePaused
        :returns : n-th frame after frame at self.timePlaying
        """
        self.timePlaying += n * self.frameLen
        self.PlManager.SetTime(self.timePlaying)
        return self.getFrame()

    def OnWxTimer(self, playing: bool, streaming: bool):
        """
        things to do in every 1/fps seconds.
        """
        if streaming:
            self.realTime = self.RTManager.GetPalyingTime()  # += self.frameLen
        if playing:
            self.timePlaying = self.PlManager.GetPalyingTime()  # += self.frameLen
