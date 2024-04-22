import wx
import cv2

from PublicFunctions import *
from ViewerPanes.StreamPlayer import *

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
        self.timer.Start(1000./15)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)
        self.Show()
        
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)
        

class ShowCapture(wx.Panel):
    def __init__(self, parent, streams: list[str], fps=60):
        super().__init__(parent)
        self.SetBackgroundColour(wx.BLACK)
        captures = [cv2.VideoCapture(c) for c in streams]
        for c in captures:
            c.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            c.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        self.drawing = False
        self.period = round(1000 / fps)
        self.playing = False

        self.player = StreamPlayer(captures, fps)
        self.timer = wx.Timer()
        self.bmp = None
        if self.SetBitmap():
            self.timer.Start(self.period)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    # Interfaces
    def Play(self):
        self.playing = True

    def Pause(self):
        self.playing = False

    def toRealTime(self, evt=None):
        self.player.setTime(0)

    def setTime(self, time: int):
        self.player.setTime(self.player.realTime - time)

    def switchStream(self, n: int):
        self.player.chooseStream(n)

    def getPlayingTime(self):
        return self.player.timePlaying

    def getTotalLength(self):
        return self.player.realTime

    def showFrame(self):
        frame = cv2.cvtColor(self.player.getFrame(), cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh()

    # Event catcher
    def OnTimer(self, evt):
        """
        runs only if this is playing
        """
        self.player.OnWxTimer(self.playing)
        if not self.playing or self.drawing:
            return
        self.showFrame()

    def OnPaint(self, evt):
        if self.bmp is None:
            return
        self.drawing = True

        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        wSize = self.GetSize()
        bmpSize = self.bmp.GetScaledSize()
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
        ret, frame = self.player.cameras[self.player.camera_no].read()
        if not ret:
            return False
            # raise ConnectionError("Connecting to stream failed")
        height, width = frame.shape[:2]
        self.GetParent().SetSize(width, height)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)

        return True

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
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    
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
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)


    # app = wx.App()
    # frame = wx.Frame(None)
    return ShowCapture2(parent, capture, fps)
    # frame.Show()
    # app.MainLoop()

if __name__ == '__main__':
    ip = '192.168.10.236'
    ip2 = '192.168.20.225'
    port = '8080'
    https_cam = f'https://{ip}:{port}/video'
    # https_cam2 = f'https://{ip2}:{port}/video'
    rtsp_cam = f'rtsp://{ip}:{port}/h264_ulaw.sdp'
    
    cam_fps = 60
    
    # cv2ShowCapture(rtsp_cam)

    app = wx.App()
    frame = wx.Frame(None)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    cap1 = wxShowCapture(frame, https_cam, cam_fps)
    # cap2 = wxShowCapture(frame, https_cam2, cam_fps)
    sizer.Add(cap1, 1, wx.EXPAND)
    # sizer.Add(cap2, 1, wx.EXPAND)
    frame.SetSizer(sizer)
    frame.Show()
    app.MainLoop()
    

