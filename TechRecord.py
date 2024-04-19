import wx
from PublicFunctions import *

class TechRecord:
    def __init__(self, begin, interval, atk, score):
        self.begin = begin
        self.interval = interval
        self.atk = atk
        self.score = score

    def renderHor(self, head: wx.Size, scale: wx.Size, gc: wx.GraphicsContext):
        gc.DrawRectangle(head[0], head[1], scale[0], scale[1])
        headStr, s = putPartString(scale)


