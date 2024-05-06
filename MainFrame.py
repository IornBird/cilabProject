import wx
import threading

from JudgeViewer import JudgeViewer
from AnalysisViewer import AnalysisViewer
from SQL import *

_ = wx.GetTranslation

class MainFrame(wx.Frame):
    def __init__(self, title: str, size):
        super().__init__(parent=None, id=wx.ID_ANY, title=title, size=size)
        self.mutex = threading.Lock()
        self.processing = False
        self.closeReq = False
        # place elements here
        self.CreateControls()

        self.analysis.importAllData()

        self.timer = wx.Timer()
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    # private
    def CreateControls(self):
        self.labs = wx.Notebook(self)
        sizer = wx.BoxSizer()
        if True:
            self.judge = JudgeViewer(self.labs)
            self.analysis = AnalysisViewer(self.labs)
        self.labs.AddPage(self.judge, "Judge Assister")
        self.labs.AddPage(self.analysis, "Contestant Analyst")
        sizer.Add(self.labs, 1, wx.EXPAND | wx.ALL)
        self.SetSizerAndFit(sizer)

        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        doStream = fileMenu.Append(wx.ID_ANY, _("Pause / Resume stream\tCtrl-P"))
        dbSetScore = fileMenu.Append(wx.ID_ANY, _("Flush Score And Reset\tCtrl-F"))

        self.Bind(wx.EVT_MENU, self.judge.OnKeyEvent, None, doStream.GetId())
        self.Bind(wx.EVT_MENU, self.judge.OnFlush, None, dbSetScore.GetId())
        menuBar.Append(fileMenu, _("&File"))
        self.SetMenuBar(menuBar)

    def DoBackgroundProcess(self):
        wx.CallAfter(self.BGProcess)

    def BGProcess(self):
        self.mutex.acquire()
        try:
            if not self.processing: return
            # all GUI changes must be in main thread
        except:
            pass
        self.mutex.release()

    """
    how events handled, and call algorithms in event handler
	examples:
    def OnButtonClicked(self, evt):
        if self.processing: return
        bck = threading.Thread(target=self.buttonJob)
        bck.start()
        bck.join()

    def buttonJob(self):
        if self.processing: return
        self.processing = True
        try:
            # code that ran in another thread
            pass
        except:
            pass
        self.processing = False
    """

    def OnTimer(self, timerEvt):
        pass

    def OnClose(self, closeEvt):
        if self.processing:
            closeEvt.Veto()
            self.closeReq = True
        else:
            self.timer.Stop()
            self.Destroy()

    def Destory(self):
        self.judge.Destroy()
        self.analysis.Destroy()
        super().Destroy()

    def loadFile(self, mess="OpenFile") -> str:
        fd = wx.FileDialog(self, mess, "", "", "All files(*.*)|*.*"
                           , wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fd.ShowModal() == wx.CANCEL:
            return ""
        return fd.GetPath()

    def saveFile(self, mess="Save as") -> str:
        fd = wx.FileDialog(self, mess, "", "", "All files(*.*)|*.*"
                           , wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fd.ShowModal() == wx.CANCEL:
            return ""
        return fd.GetPath()
