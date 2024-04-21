import wx
import time

def getNowMs():
    return time.time_ns() // 10 ** 6


def detectFont(size: list[float], panel: wx.Window, string: str, ratio=0.9):
    """
    :param size: size of rectangle
    :param panel:
    :param string: string to put into rectangle
    :param ratio:
    :return: corner of the string
    """
    textSize = panel.GetTextExtent(string)
    corner, times = putRectangle(*textSize, size, ratio)
    f = panel.GetFont()
    f.Scale(times)
    panel.SetFont(f)
    return corner


def putPartString(size: list[float], panel: wx.Window, string: str, ratio=0.9):
    """
    :param size: size of rectangle
    :param panel:
    :param string: (part of) string to put into rectangle
    :param ratio: height of string, and shown part of string
    :return:
    """
    textSize = panel.GetTextExtent(string)
    times = size[1] / textSize.y * ratio
    headY = size[1] - times * textSize.y
    s = string[:int(size[0] / textSize.x)]
    f = panel.GetFont()
    f.Scale(times)
    panel.SetFont(f)
    return headY, s


def putRectangle(rx: float, ry: float, rect: list[float], ratio=0.9):
    """
    Put biggest rectangle with (rx, ry) into center of [rect] * [ratio]
    :param rx:
    :param ry:
    :param rect:
    :param ratio:
    :return: (corner, width)
    """
    times = min(rect[0] / rx, rect[1] / ry) * ratio
    size = (rx * times, ry * times)
    corner = (
        (rect[0] - size[0]) / 2,
        (rect[1] - size[1]) / 2
    )
    return corner, times


def toInts(nums: list[float]):
    return [round(c) for c in nums]


def toTimeFormat(now):
    T = [now // 60000, now // 10]
    s = str(T[0])
    s2 = str(T[1] / 100)
    if T[1] < 1000:
        s2 = '0' + s2
    return s + ':' + s2
