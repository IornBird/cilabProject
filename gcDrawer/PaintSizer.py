import wx
# from gcDrawer.PaintObject import PaintObject


class PaintSizer:
    def __init__(self):
        self.pObjList = []

    def Add(self, pObj, proportion=0, flag=0, border=0):
        newObj = PaintObjInfo(pObj, proportion, flag, border)
        assert newObj not in self.pObjList
        self.pObjList.append(newObj)

    def makeObjSizes(self, panel):
        pass


class PaintBoxSizer(PaintSizer):
    def __init__(self, flag):
        super().__init__()
        self.flag = flag

    def makeObjSizes(self, panel):
        isV = (self.flag != wx.HORIZONTAL)
        paneAnchor = panel.pos[isV]
        refSize = [0, 0]
        propSum = 0
        for c in self.pObjList:
            p = c.pObj
            assert p.parent == panel
            if p.sizer is not None:
                p.SetSizer(p.sizer)
            if c.prop != 0:
                refSize[isV] = max(refSize[isV], c.pObj.minSize[isV])
                propSum += c.prop
            refSize[not isV] = max(refSize[not isV], c.pObj.minSize[not isV])
        v = panel.size[isV] - refSize[isV] * propSum
        refSize[isV] = max(v, refSize[isV])
        for c in self.pObjList:
            p = c.pObj
            # borders = getBorder(c.flag)
            p.pos[isV] = round(paneAnchor)
            if c.prop == 0:
                paneAnchor += p.minSize[isV]
            else:
                p.size[isV] = refSize[isV] * c.prop
                paneAnchor += p.size[isV]
            p.pos[not isV] = toCenter(p.size[not isV], refSize[not isV])
        panel.size[isV] = paneAnchor
        panel.size[not isV] = refSize[not isV]
        for c in self.pObjList:
            if c.pObj.sizer is not None and c.prop != 0:
                c.pObj.SetSizer(c.pObj.sizer)


class PaintGridBagSizer(PaintSizer):
    def __init__(self, vgap=0, hgap=0):
        raise FutureWarning("It's not finished yet")
        super().__init__()
        self.pObjList = []

    def Add(self, pObj, pos, span=wx.DefaultSpan, flag=0, border=0):
        newObj = PaintObjInfo(pObj, 0, flag, border, pos, border)
        assert newObj not in self.pObjList
        self.pObjList.append(newObj)

    def makeObjSizes(self, panel):
        sizes = [dict(), dict()]
        for c in self.pObjList:
            for b in (0, 1):
                sizes[b][c.pos[b]] = 0
                sizes[b][c.pos[b]] = max(sizes[b][c.pos[b]], c.pObj.minSize[b] / c.span[b])


    def FindItemAtPoint(pt: wx.Size):
        pass

    def FindItemAtPosition(pos: wx.Size):
        pass

def toCenter(panelLen, ontoLen):
    return round((ontoLen - panelLen) / 2)


def getBorder(flag):
    """
    :param flag:
    :return: need border on [top, bottom, left, right]
    """
    return [
        bool(flag & wx.TOP),
        bool(flag & wx.BOTTOM),
        bool(flag & wx.LEFT),
        bool(flag & wx.RIGHT)
    ]


class PaintObjInfo:
    def __init__(self, pObj, proportion, flag, border, pos=None, span=None):
        self.pObj = pObj
        self.prop = proportion
        self.flag = flag
        self.border = border
        self.pos = pos
        self.span = span

    def __eq__(self, other):
        return self.pObj == other.pObj


def putRectangle(r: list[float], rect: list[float], ratio=0.9):
    """
    Put biggest rectangle with (rx, ry) into center of [rect] * [ratio]
    :param rx:
    :param ry:
    :param rect:
    :param ratio:
    :return: (corner, width)
    """
    times = min(rect[0] / r[0], rect[1] / r[1]) * ratio
    size = (r[0] * times, r[1] * times)
    corner = (
        (rect[0] - size[0]) / 2,
        (rect[1] - size[1]) / 2
    )
    return corner, times
