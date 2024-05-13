import multiprocessing

from MainFrame import *
from Streamers.SharedData import *

if __name__ == '__main__':
    # global SD
    # SD = SharedData(multiprocessing.Manager(), 640, 480)
    app = wx.App()
    frame = MainFrame("Title", (1024, 768))
    frame.Show()
    app.MainLoop()
