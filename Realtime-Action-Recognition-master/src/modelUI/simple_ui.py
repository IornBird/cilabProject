# -*- coding: utf-8 -*-


import cv2
import wx
import wx.xrc
import threading

# from UI.mysql_api import *
from mysql_api import *
if True:
    import sys
    # sys.path.insert(0, '/home/')
    sys.path.append(fr'D:\NCU\Special_Project\Realtime-Action-Recognition\Realtime-Action-Recognition-master\src')
    from s5_test import s5_test_main

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent, capture=None ):
		wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="wx.EmptyString", pos=wx.DefaultPosition,
		                  size=wx.Size(600, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_m_panel = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook5 = wx.Notebook( self.m_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		self.InsertTab = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_InsertTab = wx.BoxSizer( wx.VERTICAL )

		# Contestant ID
		bSizer_ContestantID = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_ContestantID = wx.StaticText( self.InsertTab, wx.ID_ANY, u"Contestant ID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_ContestantID.Wrap(-1)
		bSizer_ContestantID.Add(self.m_staticText_ContestantID, 0, wx.ALL, 5)
		self.Insert_ContestantID = wx.TextCtrl( self.InsertTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_ContestantID.Add(self.Insert_ContestantID, 0, wx.ALL, 5)

		bSizer_InsertTab.Add(bSizer_ContestantID, 1, wx.EXPAND, 5)

		# Contestant Name
		bSizer_ContestantName = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_ContestantName = wx.StaticText( self.InsertTab, wx.ID_ANY, u"Contestant Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_ContestantName.Wrap(-1)
		bSizer_ContestantName.Add(self.m_staticText_ContestantName, 0, wx.ALL, 5)
		self.Insert_ContestantName = wx.TextCtrl( self.InsertTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_ContestantName.Add(self.Insert_ContestantName, 0, wx.ALL, 5)

		bSizer_InsertTab.Add(bSizer_ContestantName, 1, wx.EXPAND, 5)

		# Nationality
		bSizer_Nationality = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_Nationality = wx.StaticText( self.InsertTab, wx.ID_ANY, u"Nationality", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_Nationality.Wrap(-1)
		bSizer_Nationality.Add(self.m_staticText_Nationality, 0, wx.ALL, 5)
		self.InsertTab_Nationality = wx.TextCtrl( self.InsertTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_Nationality.Add(self.InsertTab_Nationality, 0, wx.ALL, 5)

		bSizer_InsertTab.Add(bSizer_Nationality, 1, wx.EXPAND, 5)

		# Insert Button
		bSizer_InsertBtn = wx.BoxSizer(wx.VERTICAL)
		self.InsertBtn = wx.Button( self.InsertTab, wx.ID_ANY, u"Insert", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.InsertBtn.Bind(wx.EVT_BUTTON, onInsertBtn)
		bSizer_InsertBtn.Add(self.InsertBtn, 0, wx.ALL, 5)

		bSizer_InsertTab.Add(bSizer_InsertBtn, 1, wx.EXPAND, 5)

		# Show Button
		bSizer_ShowBtn = wx.BoxSizer(wx.VERTICAL)
		self.ShowBtn = wx.Button( self.InsertTab, wx.ID_ANY, u"Show", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ShowBtn.Bind(wx.EVT_BUTTON, onShowBtn)
		bSizer_ShowBtn.Add(self.ShowBtn, 0, wx.ALL, 5)

		bSizer_InsertTab.Add(bSizer_ShowBtn, 1, wx.EXPAND, 5)
  
		# Show Label
		bSizer_ShowLabel = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_ShowLabel = wx.StaticText( self.InsertTab, wx.ID_ANY, u"Show Label: \n", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_ShowLabel.Wrap(-1)
		bSizer_ShowLabel.Add(self.m_staticText_ShowLabel, 0, wx.ALL, 5)

		bSizer_InsertTab.Add(bSizer_ShowLabel, 1, wx.EXPAND, 5)
  
		# InsertTab
		self.InsertTab.SetSizer(bSizer_InsertTab)
		self.InsertTab.Layout()
		bSizer_InsertTab.Fit(self.InsertTab)
		self.m_notebook5.AddPage( self.InsertTab, u"Insert", True )
		# self.ShowTab = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		

		
		self.VideoTab = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_VideoTab = wx.BoxSizer( wx.VERTICAL )

		# Video Info
		bSizer_VideoInfo = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_VideoInfo = wx.StaticText( self.VideoTab, wx.ID_ANY, u"Video Info: \n", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_VideoInfo.Wrap(-1)
		bSizer_VideoInfo.Add(self.m_staticText_VideoInfo, 0, wx.ALL, 5)

		bSizer_VideoTab.Add(bSizer_VideoInfo, 1, wx.EXPAND, 5)
  
  
		# Model Path
		bSizer_ModelPath = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_ModelPath = wx.StaticText( self.VideoTab, wx.ID_ANY, u"Model Path", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_ModelPath.Wrap(-1)
		bSizer_ModelPath.Add(self.m_staticText_ModelPath, 0, wx.ALL, 5)
		self.Insert_ModelPath = wx.TextCtrl( self.VideoTab, wx.ID_ANY, "model/trained_classifier.pickle", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_ModelPath.Add(self.Insert_ModelPath, 0, wx.ALL, 5)

		bSizer_VideoTab.Add(bSizer_ModelPath, 1, wx.EXPAND, 5)
  
		# Data Type
		bSizer_DataType = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_DataType = wx.StaticText(self.VideoTab, wx.ID_ANY, u"Data Type", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText_DataType.Wrap(-1)
		bSizer_DataType.Add(self.m_staticText_DataType, 0, wx.ALL, 5)
		self.Insert_DataType = wx.TextCtrl(self.VideoTab, wx.ID_ANY, "video", wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer_DataType.Add(self.Insert_DataType, 0, wx.ALL, 5)

		bSizer_VideoTab.Add(bSizer_DataType, 1, wx.EXPAND, 5)
  
		# Data Path
		bSizer_DataPath = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_DataPath = wx.StaticText(self.VideoTab, wx.ID_ANY, u"Data Path", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText_DataPath.Wrap(-1)
		bSizer_DataPath.Add(self.m_staticText_DataPath, 0, wx.ALL, 5)
		self.Insert_DataPath = wx.TextCtrl(
			self.VideoTab, wx.ID_ANY, "..\..\Taekwondo_media\self_rec\FHD-240FPS\cut\BackKickRight\BackKickRight_8.mp4", wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer_DataPath.Add(self.Insert_DataPath, 0, wx.ALL, 5)

		bSizer_VideoTab.Add(bSizer_DataPath, 1, wx.EXPAND, 5)
  
		# Output Folder
		bSizer_OutputFolder = wx.BoxSizer(wx.HORIZONTAL)
		self.m_staticText_OutputFolder = wx.StaticText(self.VideoTab, wx.ID_ANY, u"Output Folder", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText_OutputFolder.Wrap(-1)
		bSizer_OutputFolder.Add(self.m_staticText_OutputFolder, 0, wx.ALL, 5)
		self.Insert_OutputFolder = wx.TextCtrl(self.VideoTab, wx.ID_ANY, "output", wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer_OutputFolder.Add(self.Insert_OutputFolder, 0, wx.ALL, 5)
  
		bSizer_VideoTab.Add(bSizer_OutputFolder, 1, wx.EXPAND, 5)

		# Play Button
		bSizer_PlayBtn = wx.BoxSizer(wx.HORIZONTAL)
		self.PlayBtn = wx.Button( self.VideoTab, wx.ID_ANY, u"Play", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.PlayBtn.Bind(wx.EVT_BUTTON, onPlayBtn)
		bSizer_PlayBtn.Add(self.PlayBtn, 0, wx.ALL, 5)

		bSizer_VideoTab.Add(bSizer_PlayBtn, 1, wx.EXPAND, 5)


		self.VideoTab.SetSizer(bSizer_VideoTab)
		self.VideoTab.Layout()
		bSizer_VideoTab.Fit(self.VideoTab)
		self.m_notebook5.AddPage( self.VideoTab, u"Video", False )

		bSizer_m_panel.Add( self.m_notebook5, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel.SetSizer( bSizer_m_panel )
		self.m_panel.Layout()
		bSizer_m_panel.Fit( self.m_panel )
		bSizer2.Add( self.m_panel, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )
  
		# videoStream(self)
		self.Show()
		# self.SetSizerAndFit(bSizer2)

	def __del__( self ):
		pass

	def OnClose(self, event):
		self.Destroy()
  
	def videoStream(self):
		videoWarper = wx.StaticBox(self, label="Video", size=(640, 480))
		videoBoxSizer = wx.StaticBoxSizer(videoWarper, wx.VERTICAL)
		videoFrame = wx.Panel(self, -1, size=(640, 480))
		cap = ShowCapture(videoFrame, self.capture)
		videoBoxSizer.Add(videoFrame, 0)
		self.bSizer2.Add(videoBoxSizer, 0)


def onInsertBtn(event):
	print("Insert Button pressed.")

	iContestantID = str(frame0.Insert_ContestantID.GetValue())
	iContestantName = str(frame0.Insert_ContestantName.GetValue())
	iNationality = str(frame0.InsertTab_Nationality.GetValue())
	print(f'{iContestantID=}\n{iContestantName=}\n{iNationality=}')

	InsertValues = (iContestantID, iContestantName, iNationality)
	# InsertValues = (iContestantName, iNationality)
	insert_db('contestant', InsertValues)


def onShowBtn(event):
	print("Show Button pressed.")

	iContestantID = str(frame0.Insert_ContestantID.GetValue())
	print(f'{iContestantID=}')

	ShowValues = select_db('contestant', '*', f'id={iContestantID}')
	print(f'{ShowValues=}')
	frame0.m_staticText_ShowLabel.SetLabel(f'Show Label: {ShowValues}')


def onPlayBtn(event):
    print("Play Button pressed.")

    iModelPath = str(frame0.Insert_ModelPath.GetValue())
    iDataType = str(frame0.Insert_DataType.GetValue())
    iDataPath = str(frame0.Insert_DataPath.GetValue())
    iOutputFolder = str(frame0.Insert_OutputFolder.GetValue())
    print(f'{iModelPath=}\n{iDataType=}\n{iDataPath=}\n{iOutputFolder=}')

    # s5_test_main(iModelPath, iDataType, iDataPath, iOutputFolder)
    # video_thread = videoThread()
    # video_thread.start()
    t = threading.Thread(target=s5_test_main, args=(iModelPath, iDataType, iDataPath, iOutputFolder), daemon=True)
    t.start()





class GUIThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        # import wx
        app = wx.App()
        frame0 = MyFrame1(None)
        frame0.Show() # frame0.Show(True)
        app.MainLoop()

class videoThread(threading.Thread):
	def __init__(self, frame0=None):
		threading.Thread.__init__(self)
		self.daemon = True
		# self.frame0 = frame0

	def run(self, s5_test_args):
		# self.frame0.videoStream()
		s5_test_main(*s5_test_args)

class ShowCapture(wx.Panel):
	def __init__(self, parent, capture, fps=24):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (640, 480))

		self.capture = capture
		ret, frame = self.capture.read()

		height, width = frame.shape[:2]

		parent.SetSize((width, height))

		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		self.bmp = wx.BitmapFromBuffer(width, height, frame)

		self.timer = wx.Timer(self)
		self.timer.Start(1000./fps)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_TIMER, self.NextFrame)


	def OnPaint(self, evt):
		dc = wx.BufferedPaintDC(self)
		dc.DrawBitmap(self.bmp, 0, 0)

	def NextFrame(self, event):
		ret, frame = self.capture.read()
		if ret:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			self.bmp.CopyFromBuffer(frame)
			self.Refresh()




# db = MySQLdb.connect(host="localhost", user="root", password="NCUCSIE", db="test1016HW")
# with db:
# 	cur = db.cursor()
# 	failed_trigger = "CREATE trigger failed_trigger AFTER INSERT ON enrollment FOR EACH ROW BEGIN IF NEW.score < 60 THEN INSERT INTO reminders(SID, CID) VALUES(NEW.SID, NEW.CID); END IF; END"
# 	cur.execute(failed_trigger)
# 	db.commit()


if __name__ == '__main__':
	# gui_thread = GUIThread()
	# gui_thread.start()
	app = wx.App()
	frame0 = MyFrame1(None)
	frame0.Show()  # frame0.Show(True)
	app.MainLoop()
