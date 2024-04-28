import wx
from TechRecord import *


class ScoreSetPane(wx.Panel):
    def __init__(self, parent, techRecord, scores):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.TimeLabel = wx.StaticText(self, wx.ID_ANY, u"Score Set", wx.DefaultPosition, wx.DefaultSize, 0)
        self.TimeLabel.Wrap(-1)
        bSizer1.Add(self.TimeLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.blueScore = ScoreSet(self, techRecord[0][1], scores[0], True)
        bSizer1.Add(self.blueScore, 1, wx.EXPAND | wx.ALL, 5)

        self.redScore = ScoreSet(self, techRecord[1][1], scores[1], False)
        bSizer1.Add(self.redScore, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(bSizer1)
        self.Layout()

        # datas
        self.techList = techRecord  # pointer of tech-record on JudgeViewer
        self.scores = scores
        self.time = 0

        self.initScore(self.scores, self.techList)

    # Interfaces
    def setTime(self, time: int, modify=False):
        self.time = time
        if modify:
            self.blueScore.updateInterface(time)
            self.redScore.updateInterface(time)

    def setTechRecoed(self, record: tuple):
        """
        :param record: pointer of tech-record on JudgeViewer
        """
        self.techList = record

    def updateScores(self, diff, isBlue):
        self.scores[not isBlue][0] += diff[0] + diff[1]
        self.scores[isBlue][0] += diff[1]
        self.scores[not isBlue][1] += diff[1]

    def findTech(self, time: int):
        """
        find tech used on both side at time
        :param time: time since round begins, in ms
        :return: indexes of [tech of blue, tech of red]. Any of them be None if not found
        """

    def setTech(self, redTech, blueTech):
        """
        :param redTech, blueTech: id of tech used on both side at time, found in JudgeViewer.Timeline
            e.g. if (0, 1) passed, that means record[0][0] and record[0][1] will be used
        """

    # Private Functions
    def initScore(self, scores: tuple[int, int], techList):
        """
        :param scores: ([score, violate], [score, violate])
        :param techList: ([name, tech], [name, tech])
        """
        for i in range(2):
            for c in techList[i][1]:
                s = c.score
                if s < 0:
                    scores[1 - i][0] += 1
                    scores[i][1] += 1
                else:
                    scores[i][0] += s

class ScoreSet(wx.Panel):
    def __init__(self, parent, techList, scores, isBlue):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(619, 148),
                          style=wx.TAB_TRAVERSAL)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        # gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.nameTag = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.nameTag.SetBackgroundColour(wx.BLUE if isBlue else wx.RED)
        gbSizer1.Add(self.nameTag, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.techLabel = wx.StaticText(self, wx.ID_ANY, u"Tech", wx.DefaultPosition, wx.DefaultSize, 0)
        self.techLabel.Wrap(-1)
        gbSizer1.Add(self.techLabel, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.towardLabel = wx.StaticText(self, wx.ID_ANY, u"toward", wx.DefaultPosition, wx.DefaultSize, 0)
        self.towardLabel.Wrap(-1)
        gbSizer1.Add(self.towardLabel, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        techSelectChoices = [u"Punch", u"Kick", u"T. Kick", u"Gam-jeom"]
        self.techSelect = wx.ComboBox(self, wx.ID_ANY, u"Choose Tech", wx.DefaultPosition, wx.DefaultSize,
                                      techSelectChoices, 0)
        gbSizer1.Add(self.techSelect, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        towardSelectChoices = [u"Trunk", u"Head"]
        self.towardSelect = wx.ComboBox(self, wx.ID_ANY, u"Choose toward", wx.DefaultPosition, wx.DefaultSize,
                                        towardSelectChoices, 0)
        gbSizer1.Add(self.towardSelect, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.setValid = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(u"Images/notInvalid.png", wx.BITMAP_TYPE_ANY),
                                        wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        gbSizer1.Add(self.setValid, wx.GBPosition(1, 2), wx.GBSpan(2, 1), wx.ALL | wx.EXPAND, 5)

        self.sendConfirm = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(u"Images/confirm.png", wx.BITMAP_TYPE_ANY),
                                           wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        gbSizer1.Add(self.sendConfirm, wx.GBPosition(1, 3), wx.GBSpan(2, 1), wx.ALL | wx.EXPAND, 5)

        gbSizer1.AddGrowableCol(1)
        # gbSizer1.AddGrowableRow(0)
        gbSizer1.AddGrowableRow(1, 1)
        gbSizer1.AddGrowableRow(2, 1)

        self.SetSizer(gbSizer1)
        self.Layout()

        # data structure
        self.techList = techList
        self.isBlue = isBlue
        # Connect Events
        self.setValid.Bind(wx.EVT_BUTTON, self.OnValidSet)
        self.sendConfirm.Bind(wx.EVT_BUTTON, self.OnConfirm)

    # Interfaces
    def FindTech(self, time: int):
        """
        :param time: time since contest begin in ms
        :return: index of tech used at time, -1 if not found
        """
        for i, c in enumerate(self.techList):
            if c.time <= time <= c.time + 1000:
                return i
        return -1

    def updateRecord(self, time: int):
        index = self.FindTech(time)
        if index != -1:
            c = self.techList[index]
            diff = c.setValue(self.techSelect.GetValue(), self.towardSelect.GetValue())
            self.GetParent().updateScores(diff, self.isBlue)
        else:
            self.techList.append(TechRecord(time, self.techSelect.GetValue(), self.towardSelect.GetValue()))
            new = self.techList[-1]
            assert isinstance(new, TechRecord)
            diff = [new.score, (new.score < 0)]
            self.GetParent().updateScores(diff, self.isBlue)

    def updateInterface(self, time: int):
        self.setInterface(self.FindTech(time))

    # Event catcher
    def OnValidSet(self, event):
        index = self.FindTech(self.GetParent().time)
        diff = self.techList[index].reverseInvalid()
        self.setValid.SetBitmap(wx.Bitmap(u"Images/isInvalid.png" if diff[0] < 0
                                          else u"Images/notInvalid.png",
                                          wx.BITMAP_TYPE_ANY))
        self.GetParent().updateScores(diff, self.isBlue)


    def OnConfirm(self, evt):
        self.updateRecord(self.GetParent().time)

    # Private Functions
    def setInterface(self, index):
        if index == -1:
            self.techSelect.SetValue(u"Choose Tech")
            self.towardSelect.SetValue(u"Choose toward")
        else:
            c = self.techList[index]
            self.techSelect.SetSelection(Tech.FindTechRev[c.tech])
            self.towardSelect.SetSelection(Tech.FindTowardRev[c.toward])

