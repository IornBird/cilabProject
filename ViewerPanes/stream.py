from typing import Literal
import wx
import cv2



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
    def __init__(self, parent, capture, fps=15):
        wx.Panel.__init__(self, parent)

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        parent.SetSize((width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # self.bmp = wx.BitmapFromBuffer(width, height, frame)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)
        # self.bmp = wx.Bitmap.FromBufferAndAlpha(width, height, frame)
        
        self.fps = fps
        print(f'{fps=}')
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.timer = wx.Timer(self)
        # self.timer.Start(1000./self.fps)
        self.timer.Start(int(1000/self.fps))


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
            # time.sleep(1/self.fps)


def cv2ShowCapture(cam, w=320, h=240, fps=15):
    capture = cv2.VideoCapture(cam)
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
        # time.sleep(1/fps)
    capture.release()
    cv2.destroyAllWindows()

def wxShowCapture(parent, cam, fps=15):
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
    ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
    sys.path.append(ROOT)
    import importlib
    s5_test = importlib.import_module('Realtime-Action-Recognition-master.src.s5_test')
    s5_test_main = s5_test.s5_test_main
    import threading
    
    model_path = fr'D:\NCU\Special_Project\cilabProject\Realtime-Action-Recognition-master\model\trained_classifier.pickle'
    data_type = fr'video'
    video_path = fr'D:\NCU\Special_Project\Taekwondo_media\self_rec\FHD-240FPS\cut\BackKickLeft\BackKickLeft_12.mp4'
    output_path = fr'D:\NCU\Special_Project\cilabProject\Realtime-Action-Recognition-master\output'
    out_folder = video_path.split('\\')[-1][: -4]
    out_vid_path = output_path +  '\\' + out_folder + '\\' + out_folder + '.avi'
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
    https_cam2 = f'https://{ip2}:{port}/video'
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
    
    
    
    

