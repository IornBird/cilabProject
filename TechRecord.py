import wx
from PublicFunctions import *


class TechRecord:
    def __init__(self, timeSet: int, tech, toward, score: int):
        self.time = timeSet
        self.tech = tech
        self.toward = toward
        self.score = score
        self.invalid = False

    def render_derd(self, head: wx.Size, scale: wx.Size, gc: wx.GraphicsContext):
        gc.DrawRectangle(head[0], head[1], scale[0], scale[1])
        # putPartString(scale, gc, str(self.score))

    def __gt__(self, other):
        return self.time > other.time


class Tech:
    # const
    PUNCH = 0
    KICK = 1
    T_KICK = 3

    TRUNK = 1
    HEAD = 2

    VIOLATE = -1

class TechList:
    def __int__(self):
        self.heap = [None]  # index is from 1

    def append(self, e: TechRecord):
        pass


def findScore(tech, toward):
    pass


class Heap:
    def __int__(self):
        self.v = []

    def insert(self, e):
        pass

class TechRecord_derd:
    def __init__(self, begin, interval, atk, score):
        self.begin = begin
        self.interval = interval
        self.atk = atk
        self.score = score

    def renderHor(self, head: wx.Size, scale: wx.Size, gc: wx.GraphicsContext):
        gc.DrawRectangle(head[0], head[1], scale[0], scale[1])
        headStr, s = putPartString(scale)
