# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
###########################################################################

from PublicFunctions import *


class TechToken(wx.Panel):
    def __init__(self, parent, pos, size, message):
        super().__init__(parent, pos=pos, size=size)
        # shows it's invalid of not
        self.invalidSetBtn = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(u"Images/notInvalid.png", wx.BITMAP_TYPE_ANY),
                                             wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)

        # movements
        self.techLabel = wx.StaticText(self, wx.ID_ANY, message, wx.DefaultPosition, wx.DefaultSize, 0)
        self.techLabel.Wrap(-1)
        self.techLabel.SetFont(wx.Font(16, 72, 90, 90, False, "Times New Roman"))

        # Connect Events
        self.invalidSetBtn.Bind(wx.EVT_BUTTON, self.setInvalid)

    # Event handlers
    def setInvalid(self, event):
        # TODO: set image to u"Images/isInvalid.png"
        event.Skip()

    # Private functions
    def setFont(self):
        p = self.techLabel
        detectFont(p.GetSize(), p, p.GetLabelText())

    # Destructor
    def Destroy(self):
        super().Destroy()


###########################################################################
## Class TechTokenV
###########################################################################

class TechTokenV(TechToken):

    def __init__(self, parent, pos, size, message, time):
        super().__init__(parent, pos, size, message)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.timeLabel = wx.StaticText(self, wx.ID_ANY, u"0: 00.00", wx.DefaultPosition, wx.DefaultSize, 0)
        self.timeLabel.Wrap(-1)
        self.timeLabel.SetFont(wx.Font(12, 72, 90, 90, False, "Times New Roman"))

        gbSizer1.Add(self.timeLabel, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        gbSizer1.Add(self.techLabel, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.scoreLabel = wx.StaticText(self, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0)
        self.scoreLabel.Wrap(-1)
        self.scoreLabel.SetFont(wx.Font(36, 72, 90, 90, False, "Times New Roman"))

        gbSizer1.Add(self.scoreLabel, wx.GBPosition(0, 1), wx.GBSpan(2, 1), wx.ALL | wx.EXPAND, 5)

        gbSizer1.Add(self.invalidSetBtn, wx.GBPosition(0, 2), wx.GBSpan(2, 1), wx.ALL | wx.EXPAND, 5)

        gbSizer1.AddGrowableCol(0)
        gbSizer1.AddGrowableCol(2)
        gbSizer1.AddGrowableRow(1)

        self.SetSizer(gbSizer1)
        self.Layout()

    # Private functions
    def setFont(self):
        for p in [self.techLabel, self.scoreLabel, self.timeLabel]:
            detectFont(p.GetSize(), p, p.GetLabelText())


###########################################################################
## Class TechTokenH
###########################################################################

class TechTokenH(TechToken):
    def __init__(self, parent, pos, size, message):
        super().__init__(parent, pos, size, message)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2.Add(self.invalidSetBtn, 0, wx.ALL | wx.EXPAND, 5)

        bSizer2.Add(self.techLabel, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()

    # Private functions
    def setFont(self):
        super().setFont()
