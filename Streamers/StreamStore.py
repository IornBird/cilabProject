import cv2

import multiprocessing
import time
from TimeManager import TimeManager
from PublicFunctions import timeTag

from Streamers.SharedData import SharedData

import os
import sys
OPENPOSE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../Realtime-Action-Recognition-master/src"
sys.path.append(OPENPOSE_PATH)
from s5_test import s5_test_main

# E:\專題\JudgeWatcer\Realtime-Action-Recognition-master\src\s5_test.py

'''
s5_test_main(model_path, data_type, data_path, output_folder, img_displayer_on)

args are all str, img_displayer_on is bool, True iff show frame in other window

--model_path Realtime-Action-Recognition-master/model/trained_classifier.pickle
--data_type webcam
--data_path 'https://192.168.0.12:8080/video' `
--output_folder output/webcam

--model_path model/trained_classifier.pickle
--data_type video
--data_path ..../Taekwondo_media/video/video-11m14s-31-x3htXTI7nDI.mp4 
--output_folder output 
'''


class StreamStore2:
    def __init__(self, streamSource: str| int, SD: SharedData):
        self.SD = SD

        self.streamSrc = streamSource
        self.recording_process = None
        self.id = SD.createNew()

    def Play(self):
        if self.recording_process is None or not self.recording_process.is_alive():
            args = (
                'Realtime-Action-Recognition-master/model/trained_classifier.pickle',
                'webcam',
                self.streamSrc,
                'output/webcam',
                self.SD,
                self.id
            )
            self.recording_process = multiprocessing.Process(target=s5_test_main, args=args)
            self.recording_process.start()

    def read(self):
        frame = self.SD.getStreamFrame(self.id)
        success = frame is not None
        return success, frame

    def set(self, mode, time):
        """
        dummy, for not modifying Interfaces in other files
        """
        pass

    def Pause(self):
        """
        dummy, for not modifying Interfaces in other files
        """
        pass

    def Stop(self):
        if self.recording_process is not None and self.recording_process.is_alive():
            self.SD.STOP[0] = True
            # self.recording_process.terminate()
            self.recording_process.join()

            self.recording_process.close()
            self.recording_process = None


class VideoReader:
    def __init__(self, SD: SharedData, ID: int):
        self.SD = SD

        self.recording_process = None
        self.id = ID

        self.time = 0

    def read(self):
        frame = self.SD.getResultFrame(self.id, round(self.time * 60 / 1000))
        success = frame is not None
        return success, frame

    def set(self, mode, time):
        """
        set timer playing on Result
        """
        if mode == cv2.CAP_PROP_POS_MSEC:
            self.time = time
        else:
            self.time += round(time * 1000 / 60)

class StreamStore:
    def __init__(self, streamSource: str| int, file: str, fps=60, id=0):
        manager = multiprocessing.Manager()

        self.streamSrc = streamSource
        self.file = file

        self.recording_process = None  # will be a multiprocessing.Process
        self.fps = fps

        self.shared_Frame = manager.list()

        self.doRecord = manager.list()
        self.doProcess = manager.list()

        self.timer = manager.list()

        self.setSharedVars()
        self.id = id

    def setSharedVars(self):
        self.shared_Frame.append(None)
        self.doRecord.append(False)
        self.doProcess.append(False)
        self.timer.append(TimeManager())


    def record_frames(self):
        """
        This function will be run in a separate process.
        It continuously saves frames to the specified file.
        """
        timeTag("record")
        try:
            cap = cv2.VideoCapture(self.streamSrc)
            assert cap.isOpened()
            fourcc = cv2.VideoWriter.fourcc(*'XVID')
            out = cv2.VideoWriter(self.file, fourcc, self.fps, (640, 480))
            timer = TimeManager()
            timer.Start()
            frmNum = 0
            timeTag('[loop]')
            while self.doProcess[0]:
                if self.doRecord[0]:
                    timer.Start()
                else:
                    timer.Pause()
                ret, frame = cap.read()
                self.shared_Frame[0] = frame

                if ret and self.doRecord[0]:
                    while frmNum < (timer.GetPalyingTime()) * self.fps / 1000:
                        out.write(frame)
                        frmNum += 1

                if timer.GetPalyingTime() >= 5000:
                    out.release()
                    out = cv2.VideoWriter(self.file, fourcc, self.fps, (640, 480))
                    timer.SetTime(0)
                    frmNum = 0
                    timeTag("[re-record]")
            out.release()
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print("Exception")
            self.doProcess[0] = False

    def read(self):
        success = self.shared_Frame[0] is not None
        return success, self.shared_Frame[0]

    def set(self, mode, time):
        """
        dummy, for not modifying Interfaces in other files
        """
        pass

    def Play(self):
        """
        start or resume streaming and recording
        """
        timeTag("Play")
        if self.recording_process is None or not self.recording_process.is_alive():
            # self.recording_process = multiprocessing.Process(s5_test_main, args=...)
            self.recording_process = multiprocessing.Process(target=self.record_frames)
            self.doRecord[0] = True
            self.doProcess[0] = True
            self.recording_process.start()

    def Pause(self):
        """
        pause streaming and recording
        frame after Pause() and before Play() will be ignored
        """
        timeTag("Pause")
        if self.recording_process is not None and self.recording_process.is_alive():
            self.doRecord[0] = False

    def Stop(self):
        timeTag("Stop")
        if self.recording_process is not None and self.recording_process.is_alive():
            self.doProcess[0] = False
            print("join")
            self.recording_process.join()
            print("\tjoined")
            self.recording_process.close()
            self.recording_process = None

    def isPresent(self):
        return self.recording_process is not None and self.recording_process.is_alive()

    # Private Functions
    def canRecord(self):
        return self.recording_process is not None and self.recording_process.is_alive()


FILE = '../videos/0.avi'


def record():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter.fourcc(*'XVID')
    out = cv2.VideoWriter(FILE, fourcc, 60.0, (640, 480))
    start_time = time.time()
    frmNum = 0
    print('loop')
    while True:
        ret, frame = cap.read()
        if ret:
            while frmNum < (time.time() - start_time) * 60.0:
                out.write(frame)
                frmNum += 1
            if time.time() - start_time >= 5:
                out.release()
                cap.release()
                cv2.destroyAllWindows()
                break
        else:
            break


def canRead():
    cap = cv2.VideoCapture(FILE)
    ret, frame = cap.read()
    time.sleep(1)
    ret, frame = cap.read()
    cap.release()
    return ret


_record_test = True
if __name__ == '__main__':
    f = open(FILE, 'rb')
    print(f.read()[:10])
    f.close()
    input("Press [Enter] to continue")
    if _record_test:
        record()
        print("check if record successes")
        print(canRead())
        print("end")
    else:
        ss = StreamStore(0, FILE)
        print("record")
        ss.Play()
        time.sleep(5)
        print(f"getting frame when recording: {ss.read()[0]}")
        print(f"read video during writing: {canRead()}")
        ss.Pause()
        time.sleep(6)
        ss.Play()
        time.sleep(1)
        ss.Stop()
        print("check if record in another process successes")
        print(canRead())
        print("end")

