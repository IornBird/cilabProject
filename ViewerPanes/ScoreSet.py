import wx
from TechRecord import *

class ScoreSetPane(wx.Panel):
    def __init__(self, parent, blueTech, redTech):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.TimeLabel = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.TimeLabel.Wrap(-1)
        bSizer1.Add(self.TimeLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.blueScore = ScoreSet(self, blueTech)
        bSizer1.Add(self.blueScore, 1, wx.EXPAND | wx.ALL, 5)

        self.redScore = ScoreSet(self, redTech)
        bSizer1.Add(self.redScore, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # data structures
        self.techList = None  # pointer of tech-record on JudgeViewer

    # Interfaces
    def SetTimer(time: int):
        pass

    def setTechRecoed(self, record: tuple):
        """
        :param record: pointer of tech-record on JudgeViewer
        """
        self.techList = record

    def findTech(self, time: int):
        """
        find tech used on both side at time
        :param time: time since round begins, in ms
        :return: [tech of blue, tech of red]. Any of them be None if not found
        """

    def setTech(self, redTech, blueTech):
        """
        :param redTech, blueTech: id of tech used on both side at time, found in JudgeViewer.Timeline
            e.g. if (0, 1) passed, that means record[0][0] and record[0][1] will be used
        """


class ScoreSet(wx.Panel):
    def __init__(self, parent, techList):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(619, 148),
                          style=wx.TAB_TRAVERSAL)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.nameTag = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gbSizer1.Add(self.nameTag, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.techLabel = wx.StaticText(self, wx.ID_ANY, u"Tech", wx.DefaultPosition, wx.DefaultSize, 0)
        self.techLabel.Wrap(-1)
        gbSizer1.Add(self.techLabel, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.towardLabel = wx.StaticText(self, wx.ID_ANY, u"toward", wx.DefaultPosition, wx.DefaultSize, 0)
        self.towardLabel.Wrap(-1)
        gbSizer1.Add(self.towardLabel, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        techSelectChoices = [u"Punch", u"Kick", u"T. Kick"]
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

        gbSizer1.AddGrowableCol(1)
        gbSizer1.AddGrowableRow(0)
        gbSizer1.AddGrowableRow(1)
        gbSizer1.AddGrowableRow(2)

        self.SetSizer(gbSizer1)
        self.Layout()

        # Connect Events
        self.setValid.Bind(wx.EVT_BUTTON, self.OnValidSet)


    # Virtual event handlers, overide them in your derived class
    def OnValidSet(self, event):
        self.setValid.SetBitmap(wx.Bitmap(u"Images/notInvalid.png", wx.BITMAP_TYPE_ANY))
