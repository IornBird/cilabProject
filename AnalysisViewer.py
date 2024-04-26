###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
###########################################################################

import wx
import wx.xrc
import wx.grid

import SQL.mysql_api as sql

class AnalysisViewer(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        baseSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.anaDataPane = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        anaSizer = wx.GridBagSizer(0, 0)
        anaSizer.SetFlexibleDirection(wx.BOTH)
        anaSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.nameLabel = wx.StaticText(self.anaDataPane, wx.ID_ANY, u"Contestant Name", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.nameLabel.Wrap(-1)
        anaSizer.Add(self.nameLabel, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        defaultChoices = [u"Yume Nijino", u"Laura Sakuraba"]
        self.contestantChoice = wx.Choice(self.anaDataPane, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          defaultChoices, 0)
        self.contestantChoice.SetSelection(0)
        anaSizer.Add(self.contestantChoice, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.resultChat = wx.grid.Grid(self.anaDataPane, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.resultChat.CreateGrid(5, 1)
        self.resultChat.EnableEditing(True)
        self.resultChat.EnableGridLines(True)
        self.resultChat.EnableDragGridSize(False)
        self.resultChat.SetMargins(0, 0)

        # Columns
        self.resultChat.EnableDragColMove(False)
        self.resultChat.EnableDragColSize(True)
        self.resultChat.SetColLabelSize(30)
        self.resultChat.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.resultChat.EnableDragRowSize(True)
        self.resultChat.SetRowLabelSize(80)
        self.resultChat.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.resultChat.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        anaSizer.Add(self.resultChat, wx.GBPosition(1, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        anaSizer.AddGrowableCol(1)
        anaSizer.AddGrowableRow(1)

        self.anaDataPane.SetSizer(anaSizer)
        self.anaDataPane.Layout()
        anaSizer.Fit(self.anaDataPane)
        baseSizer.Add(self.anaDataPane, 3, wx.EXPAND | wx.ALL, 5)

        self.baseDataPane = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bDataSizer = wx.BoxSizer(wx.VERTICAL)

        self.contestantPhoto = wx.StaticBitmap(self.baseDataPane, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        bDataSizer.Add(self.contestantPhoto, 1, wx.ALL | wx.EXPAND, 5)

        self.basicChat = wx.grid.Grid(self.baseDataPane, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.basicChat.CreateGrid(5, 1)
        self.basicChat.EnableEditing(False)
        self.basicChat.EnableGridLines(True)
        self.basicChat.EnableDragGridSize(False)
        self.basicChat.SetMargins(0, 0)

        # Columns
        self.basicChat.EnableDragColMove(False)
        self.basicChat.EnableDragColSize(True)
        self.basicChat.SetColLabelSize(30)
        self.basicChat.SetColLabelValue(0, "Value")
        self.basicChat.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.basicChat.EnableDragRowSize(True)
        self.basicChat.SetRowLabelSize(80)
        self.basicChat.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.basicChat.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bDataSizer.Add(self.basicChat, 1, wx.ALL | wx.EXPAND, 5)

        self.baseDataPane.SetSizer(bDataSizer)
        self.baseDataPane.Layout()
        bDataSizer.Fit(self.baseDataPane)
        baseSizer.Add(self.baseDataPane, 2, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(baseSizer)
        self.Layout()

        self.baseCache = dict()
        self.anaCache = dict()

        # Connect Events
        self.contestantChoice.Bind(wx.EVT_CHOICE, self.OnChoiceName)

    def Destroy(self):
        super().Destroy()

    # Interfaces
    def importAllData(self):
        # SELECT * FROM `contestant`
        lst = sql.select_db('contestant', '*', '1')  # ((1, 'Yume Nijino', 'Japan'), (2, 'Vegeta', 'Planet Vegeta'))
        # self.contestantChoice.Create(self.anaDataPane, wx.ID_ANY, choices=[c[1] for c in lst])
        self.contestantChoice.Set([c[1] for c in lst])

    # Virtual event handlers, override them in your derived class
    def OnChoiceName(self, event):
        name = self.contestantChoice.GetStringSelection()
        id = sql.select_db('contestant', 'id', f"name='{name}'")[0][0]
        baseData = sql.select_db('body_stats', '*', f"contestant_id={id}")
        anaResult = sql.select_db('comp_stats', '*', f"contestant_id={id}")
        self.importOneData(name, baseData[0], anaResult[0])


    # private functions
    def getData(self):
        pass
        # importData()
        # get_contestant_status()

    def importOneData(self, name: str, baseData, analysisResult):
        """
        :param name: name of ONE contestant
        :param baseData:
        :param analysisResult:
        """
        self.changeTable(self.basicChat, baseData, ['id', 'height', 'weight'])
        self.changeTable(self.resultChat, analysisResult, [
            'ID',
            'contest_num',
            'contest_tot_secs',
            'wins',
            'win_rounds',
            'lose_rounds',
            'punches',
            'kicks',
            'suc_punches',
            'suc_kicks',
            'pts',
            'vios',
            'vio_lost_pts'
        ])
        return

        # baseChat = wx.grid.Grid(self)
        # baseChat.CreateGrid(len(baseData), 1)
        # for i, c in enumerate(baseData):
        #     baseChat.SetCellValue(i, 0, str(c))
        #
        # anaResult = wx.grid.Grid(self)
        # anaResult.CreateGrid(len(analysisResult), 1)
        # for i, c in enumerate(analysisResult):
        #     anaResult.SetCellValue(i, 0, str(c))
        #
        # # self.contestantChoice.Append(name)
        # # self.contestantChoice.SetSelection(self.contestantChoice.FindString(name, True))
        # self.basicChat.SetTable(baseChat, True)
        # self.resultChat.SetTable(anaResult, True)

    def changeTable(self, table: wx.grid.Grid, data: list[str], items: list[str]):
        """
        make data[i] to be in i-th row of table, all data are in 0-th column
        """
        current_rows = table.GetNumberRows()
        new_rows = len(data)

        # If new data has more rows, append rows
        if new_rows > current_rows:
            table.AppendRows(new_rows - current_rows)
        # If new data has fewer rows, delete rows
        elif new_rows < current_rows:
            table.DeleteRows(new_rows, current_rows - new_rows)

        # Set cell values
        for i, value in enumerate(data):
            table.SetCellValue(i, 0, str(value))
        for i, item in enumerate(items):
            table.SetRowLabelValue(i, item)
