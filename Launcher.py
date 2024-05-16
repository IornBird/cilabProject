import multiprocessing

from MainFrame import *
from Streamers.SharedData import *
import Streamers.SharedData as SD


if __name__ == '__main__':
    # global SD
    # SD = SharedData(multiprocessing.Manager(), 640, 480)
    app = wx.App()
    frame = MainFrame("Title", (1024, 768))
    try:
        frame.Show()
        SD.GUI_APP = app
        app.MainLoop()
    except Exception as e:
        frame.Destroy()
        raise e
