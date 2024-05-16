import multiprocessing

import wx

from PublicFunctions import *
from Streamers.StreamPlayer import *
from Streamers.StreamStore import *
from Streamers.SharedData import *


# this class has not used yet
class CapFrame(wx.Frame):
    def __init__(self, ip_cam):
        super().__init__(None, title='IP Camera Stream', size=(640, 480))
        panel = wx.Panel(self)
        self.capture = cv2.VideoCapture(ip_cam)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        ret, frame = self.capture.read()
        height, width = frame.shape[:2]
        # parent.SetSize((width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)
        self.timer = wx.Timer(self)
        self.timer.Start(1000. / 15)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # self.Bind(wx.EVT_TIMER, self.NextFrame)
        self.Show()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)


from Streamers.SharedData import *

SD = None


class ShowCapture(wx.Panel):
    def __init__(self, parent, streams: list[str], playbacks: list[str], fps=60):
        super().__init__(parent)
        self.SetBackgroundColour(wx.BLACK)

        SD = SharedData(multiprocessing.Manager(), self, 640, 480)
        SD = SharedData(multiprocessing.Manager(), 640, 480)

        # captures = [cv2.VideoCapture(f'https://{c}:{8080}/video') for c in streams]
        # captures = [cv2.VideoCapture('C:\\Users\\User\\Desktop\\source\\source2\\Miyabi_Love_You.mp4')]

        # captures = [StreamStore(b, f"../videos/{b}.avi", fps) for b in (0,)]
        # videos = [cv2.VideoCapture(c) for c in playbacks]
        #
        # captures = [cv2.VideoCapture(b) for b in (0,)]

        captures = [StreamStore2(b, SD) for b in (1,)]
        videos = [VideoReader(SD, i) for i in range(len(captures))]

        # self.store = [StreamStore(b, '.\\videos\\' + str(b) + '.avi', fps) for b in (0, 1)]

        # for c in captures:
        #     c.Play()
            # c.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            # c.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            # c.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*'MJPG'))
        for c in videos:
            c.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            c.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            c.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*'XVID'))

        SD.allPushed[0] = False

        self.drawing = False
        self.period = round(1000 / fps)
        self.playing = False
        self.streaming = False
        self.modified = False

        self.player = StreamPlayer(captures, videos, fps)
        self.timer = None  # wx.Timer()
        self.bmp = None
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.callOnBuilt = lambda: [self.OnGUIBuilt(SD)]
        self.SetBitmap()
        # self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        # if self.SetBitmap():
        #     self.timer.Start(self.period)

    # Interfaces
    def SetTimer(self, timer: wx.Timer):
        self.timer = timer
        # if not self.timer.IsRunning():
        #     self.timer.Start(self.period)

    def Play(self):
        timeTag("ShowCapture::Play")
        self.playing = True
        self.player.Play()

    def Pause(self):
        timeTag("ShowCapture::Pause")
        self.playing = False
        self.player.Pause()
        self.showFrame()

    def GamePlay(self):
        timeTag("ShowCapture::GamePlay")
        self.streaming = True
        self.player.RTPlay()
        # [c.Play() for c in self.store]

    def GamePause(self):
        timeTag("ShowCapture::GamePause")
        self.streaming = False
        self.player.RTPause()
        # [c.Pause() for c in self.store]
        self.showFrame()

    def toRealTime(self, evt=None):
        self.player.toStream()
        self.player.setTime(0)
        self.SetBitmap()
        self.Play()
        self.GamePlay()

    def toPlayBack(self):
        self.player.toStream(False)
        self.player.setTime(10000)
        self.SetBitmap()

    def setTime(self, time: int):
        self.player.setTime(self.player.realTime - time)

    def switchStream(self, n: int):
        self.player.chooseStream(n)
        self.SetBitmap()
        # frame = self.player.getFrame()
        # height, width = frame.shape[:2]
        # self.bmp.SetSize((width, height))

        # self.SetBitmap()

    def getPlayingTime(self):
        return self.player.timePlaying

    def getTotalLength(self):
        return self.player.realTime

    def showFrame(self):
        timeTag("ShowCapture::showFrame")
        gframe = self.player.getFrame()
        if gframe is None:
            return
        frame = cv2.cvtColor(gframe, cv2.COLOR_BGR2RGB)


        self.bmp.CopyFromBuffer(frame)
        # self.Refresh()

    # Event catcher
    def OnGUIBuilt(self, SD):
        app = None
        while app is None:
            app = wx.GetApp()
        timeTag("main: GUI built")
        SD.allPushed[0] = True
        for c in self.player.cameras:
            c.Play()
        SD.APP[0] = app

    def OnWxTimer(self, modified):
        """
        runs only if this is playing
        """
        if self.callOnBuilt is not None:
            self.callOnBuilt()
            self.callOnBuilt = None
        self.player.OnWxTimer(self.playing, self.streaming)
        if (self.playing or modified) and not self.drawing:
            self.showFrame()
            self.Refresh()

    def OnPaint(self, evt):
        if self.bmp is None:
            return
        if self.drawing:
            return
        self.drawing = True

        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        wSize = self.GetSize()
        bmpSize = self.bmp.GetSize()
        # bmpSize = self.bmp.GetScaledSize()
        corner, ratio = putRectangle(*bmpSize, wSize, 1)
        bmpSize = toInts([bmpSize.x * ratio, bmpSize.y * ratio])
        gc.DrawBitmap(self.bmp, *corner, *bmpSize)

        self.drawing = False

    def OnNextFrame(self, evt):
        if not self.playing:
            frame = cv2.cvtColor(self.player.viewNextNFrame(1), cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()

    def OnPreviousFrame(self, evt):
        if not self.playing:
            frame = cv2.cvtColor(self.player.viewNextNFrame(-1), cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()

    # Private functions
    def SetBitmap(self):
        frame = self.player.getFrame()
        if frame is None:
            return False
        # ret, frame = self.player.cameras[self.player.camera_no].read()
        # if not ret:
        #     return False
        #     # raise ConnectionError("Connecting to stream failed")
        height, width = frame.shape[:2]
        # self.GetParent().SetSize(width, height)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)

        self.Refresh()

        return True

    # Destructor
    def Destroy(self):
        self.player.Destroy()
        super().Destroy()

class ShowCapture2(wx.Panel):
    def __init__(self, parent, captures=None, fps=60):
        wx.Panel.__init__(self, parent)

        self.drawing = False
        self.period = round(1000 / fps)

        self.player = StreamPlayer(captures, fps)

        self.bmp = None  # wx.Bitmap
        # ret, frame = self.capture.read()

        # height, width = frame.shape[:2]
        # if capture is not None:
        #     self.SetBitmap(capture)

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #
        # # self.bmp = wx.BitmapFromBuffer(width, height, frame)
        # self.bmp = wx.Bitmap.FromBuffer(width, height, frame)
        # self.bmp = wx.Bitmap.FromBufferAndAlpha(width, height, frame)

        self.timer = wx.Timer(self)
        # self.timer.Start(1000./fps)
        # self.timer.Start(self.period)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnNextFrame)

    # Interfaces
    def SetCma(self, ip: str, port: str):
        cam = f'https://{ip}:{port}/video'
        capture = cv2.VideoCapture(cam)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.SetBitmap(capture)

    def Play(self):
        if not self.timer.IsRunning():
            self.timer.Start(self.period)

    def Stop(self):
        if self.timer.IsRunning():
            self.timer.Stop()

    def Destroy(self):
        self.Stop()
        super().Destroy()

    # Event catcher
    def OnPaint(self, evt):
        self.drawing = True

        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        wSize = self.GetSize()
        bmpSize = self.bmp.GetScaledSize()
        corner, ratio = putRectangle(*bmpSize, wSize, 1)
        bmpSize = toInts([bmpSize.x * ratio, bmpSize.y * ratio])
        gc.DrawBitmap(self.bmp, *corner, *bmpSize)
        # dc.DrawBitmap(self.bmp, 0, 0)

        self.drawing = False

    def OnNextFrame(self, event):
        if self.drawing:
            return
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()

    # Private functions
    def SetBitmap(self, capture):
        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        self.GetParent().SetSize(width, height)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)

        return (width, height)

def cv2ShowCapture(cam, fps=60):
    capture = cv2.VideoCapture(cam)
    w = 320
    h = 240
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    # capture.set(cv2.CAP_PROP_FPS, 15)
    fps = capture.get(cv2.CAP_PROP_FPS)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    while True:
        ret, frame = capture.read()
        if ret:
            cv2.imshow('IP Camera Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    capture.release()
    cv2.destroyAllWindows()

    
def wxShowCapture(parent, cam, fps=60):
    capture = cv2.VideoCapture(cam)
    fr = capture.read()[1]
    w, h = fr.shape[:2]
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    # capture.set(cv2.CAP_PROP_FPS, fps)
    # fps = capture.get(cv2.CAP_PROP_FPS)
    # capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    return ShowCapture(parent, capture, fps)


def test_s5():
    import sys
    import os

    ROOT = os.path.dirname(os.path.abspath(__file__)) + "/../"

    sys.path.append(ROOT)
    import importlib
    s5_test = importlib.import_module('Realtime-Action-Recognition-master.src.s5_test')
    s5_test_main = s5_test.s5_test_main

    model_path = fr'D:\NCU\Special_Project\cilabProject\Realtime-Action-Recognition-master\model\trained_classifier.pickle'
    data_type = fr'video'
    video_path = fr'D:\NCU\Special_Project\Taekwondo_media\self_rec\FHD-240FPS\cut\BackKickLeft\BackKickLeft_12.mp4'
    output_path = fr'D:\NCU\Special_Project\cilabProject\Realtime-Action-Recognition-master\output'
    out_folder = video_path.split('\\')[-1][: -4]
    out_vid_path = output_path + '\\' + out_folder + '\\' + out_folder + '.avi'

    ip = '192.168.219.229'
    port = '8080'
    https_cam = f'https://{ip}:{port}/video'

    # s5_test_main_args = (model_path, data_type, video_path, output_path)
    s5_test_main_args = (model_path, 'webcam', https_cam, output_path + fr'\webcam', True)
    # s5_test_main_thread = threading.Thread(target=s5_test_main, args=s5_test_main_args)
    # s5_test_main_thread.start()
    s5_test_main(*s5_test_main_args)
    # wx_model_output_args = (out_vid_path, 240)
    # app = wx.App()
    # frame = wx.Frame(None)
    # model_out = wxShowCapture(frame, *wx_model_output_args)
    # frame.Show()
    # app.MainLoop()


def test_ip_cam():
    ip = '192.168.219.229'
    ip2 = '192.168.20.225'
    port = '8080'
    # cv2.VideoCapture('rtsp://username:password@192.168.1.64/1')
    https_cam = f'https://{ip}:{port}/video'
    # https_cam2 = f'https://{ip2}:{port}/video'
    rtsp_cam = f'rtsp://{ip}:{port}/h264_ulaw.sdp'

    # cv2ShowCapture(https_cam)

    app = wx.App()
    frame = wx.Frame(None)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    cap1 = wxShowCapture(frame, https_cam, 30)
    # cap2 = wxShowCapture(frame, https_cam2)
    sizer.Add(cap1, 1, wx.EXPAND)
    # sizer.Add(cap2, 1, wx.EXPAND)
    frame.SetSizer(sizer)
    frame.Show()
    app.MainLoop()

    
if __name__ == '__main__':
    # test_ip_cam()

    test_s5()
