import wx
import cv2

from PublicFunctions import *

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
    def __init__(self, parent, capture, fps=60):
        wx.Panel.__init__(self, parent)

        self.drawing = False

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        parent.SetSize((width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # self.bmp = wx.BitmapFromBuffer(width, height, frame)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)
        # self.bmp = wx.Bitmap.FromBufferAndAlpha(width, height, frame)
        

        self.timer = wx.Timer(self)
        # self.timer.Start(1000./fps)
        self.timer.Start(int(1000/fps))


        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

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

    def NextFrame(self, event):
        if self.drawing:
            return
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()

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
    return ShowCapture(parent, capture, fps)
    # frame.Show()
    # app.MainLoop()

if __name__ == '__main__':
    ip = '192.168.0.2'
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
    

