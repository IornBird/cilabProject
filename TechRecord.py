import wx
from PublicFunctions import *


class TechRecord:
    def __init__(self, timeSet: int, tech, toward):
        self.time = timeSet
        self.tech = 0
        self.toward = 0
        self.score = 0
        self.setValue(tech, toward)
        self.invalid = False

    @staticmethod
    def create(time, tech_5s, toward_5s):
        return TechRecord(time,
                    Tech.FindFrom5s[tech_5s[1:]],
                    Tech.FindFrom5s[toward_5s]
               )

    def setValue(self, tech, toward):
        """
        :return: change of [score, violate], used for total score change
        """
        if isinstance(tech, str):
            tech = Tech.FindTech[tech]
        if isinstance(toward, str):
            toward = Tech.FindToward[toward]
        dViolate = (tech == Tech.VIOLATE) - (self.tech == Tech.VIOLATE)
        self.tech = tech
        self.toward = toward
        dScore = self.score
        self.score = findScore(tech, toward)
        return [self.score - dScore, dViolate]

    def reverseInvalid(self):
        """
        :return: change of [score, violate], used for total score change
            if score is negative, self is now invalid
        """
        self.invalid = not self.invalid
        neg = -1 if self.invalid else 1
        return [neg * self.score, neg * (self.tech == Tech.VIOLATE)]

    def getScore(self):
        return findScore(self.tech, self.toward)

    def __eq__(self, other):
        teq = (self.tech == other.tech)
        return teq and (self.toward == self.toward or self.tech == Tech.VIOLATE)

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

    FindTech = {
        'Punch': PUNCH,
        'Kick': KICK,
        'T. Kick': T_KICK,
        'Gam-jeom': VIOLATE
    }
    FindTechRev = {
        PUNCH: 0,
        KICK: 1,
        T_KICK: 2,
        VIOLATE: 3
    }
    FindToward = {
        'Trunk': TRUNK,
        'Head': HEAD
    }
    FindTowardRev = {
        TRUNK: 0,
        HEAD: 1
    }

    FindFrom5s = {
        'wrist': PUNCH,
        'ankle': KICK,

        'head': HEAD,
        'body': TRUNK
    }


class TechList:
    def __int__(self):
        self.heap = [None]  # index is from 1

    def append(self, e: TechRecord):
        pass


def findScore(tech: int, toward: int):
    """
    3.1 One (1) point for a valid punch to the trunk protector
        1 分: 有效正拳技術擊中軀幹護具。
    3.2 Two (2) points for a valid kick to the trunk protector
        2 分: 有效踢擊技術擊中軀幹護具 (1 + 1)
    3.3 Three (4) points for a valid turning kick to the trunk protector
        4 分: 有效轉身踢擊技術擊中軀幹護具。 (3 + 1)
    3.4 Three (3) points for a valid kick to the head
        3 分: 有效踢擊技術擊中頭部。 (1 + 2)
    3.5 Four (5) points for a valid turning kick to the head
        5 分: 轉身踢擊技術有效擊中頭部。 (3 + 2)
    3.6 One (1) point awarded for or every one Gam-jeom given to the opponent contestant
        由於對手被” Gam-jeom” 判罰而獲得 1 分。
    :param tech:
    :param toward:
    :return:
    """
    if tech == Tech.PUNCH:
        return int(toward == Tech.TRUNK)
    elif tech == Tech.VIOLATE:
        return -1
    return tech + toward


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
