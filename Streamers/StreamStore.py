import cv2

import multiprocessing
import time

class StreamStore:
    def __init__(self, streamSource: str| int, file: str, fps=60):
        # self.capture = cv2.VideoCapture(streamSource)
        self.streamSrc = streamSource
        self.file = file
        # f = open(self.file, 'wb')
        # f.write(bytes([97, 98, 99]))
        # f.close()
        manager = multiprocessing.Manager()
        self.shared_Frame = manager.list()
        self.shared_Frame.append(None)
        self.recording_process = None  # will be a multiprocessing.Process
        self.fps = fps
        self.doRelease = manager.list()
        self.doRelease.append(False)
        self.running = False

    def record_frames(self):
        """
        This function will be run in a separate process.
        It continuously saves frames to the specified file.
        """
        print("record")
        try:
            capture = cv2.VideoCapture(self.streamSrc)
            print("capture set for", self.file)
            # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            out = cv2.VideoWriter(self.file, cv2.VideoWriter.fourcc(*'XVID'), self.fps, (320, 240))
            start_time = time.time()
            print('loop')
            while True:
                ret, frame = capture.read()
                if ret:
                    out.write(frame)
                    self.shared_Frame.__setitem__(0, frame)
                    print("\twritten")
                if time.time() - start_time >= 5:# or self.doRelease:
                    capture.release()
                    out.release()
                    cv2.destroyAllWindows()
                    print("return")
                    return
                    # out = cv2.VideoWriter(self.file, cv2.VideoWriter.fourcc(*'mp4v'), self.fps, (320, 240))
                    # start_time = time.time()
        except Exception as e:
            print("Exception")
            self.running = False
            return

    def read(self):
        return self.shared_Frame[0]

    def Play(self):
        """
        start or resume streaming and recording
        """
        if self.recording_process is None or not self.recording_process.is_alive():
            self.recording_process = multiprocessing.Process(target=self.record_frames)
            self.doRelease = False
            self.running = True
            self.recording_process.start()
            print("join")
            self.recording_process.join()
            self.recording_process.close()
            print("\tjoined")
            self.recording_process = None


    def Pause(self):
        """
        pause streaming and recording
        frame after Pause() and before Play() will be ignored
        """
        if self.recording_process is not None and self.recording_process.is_alive():
            self.shared_Frame.__setitem__(0, True)
            # self.doRelease = True
            print("join")
            self.recording_process.join()
            print("\tjoined")
            self.recording_process.close()
            self.recording_process = None


def sleep(t):
    dt = time.time() + t
    while time.time() < dt:
        pass


if __name__ == '__main__':
    f = open('../videos/0.avi', 'rt')
    print(f.read())
    # f.write(bytes([97, 98, 99]))
    f.close()
    input("Press [Enter] to continue")
    ss = StreamStore(0, '../videos/0.avi')
    print("play starts")
    #ss.Play()
    ss.record_frames()
    print("end")
    # print("wait for 6 sec")
    # sleep(10)
    # print("pause")
    # ss.Pause()
    # print("end")
