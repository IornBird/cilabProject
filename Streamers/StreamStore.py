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
            cap = cv2.VideoCapture(self.streamSrc)
            fourcc = cv2.VideoWriter.fourcc(*'XVID')
            out = cv2.VideoWriter(self.file, fourcc, self.fps, (640, 480))
            start_time = time.time()
            frmNum = 0
            print('loop')
            while True:
                ret, frame = cap.read()
                if ret:
                    while frmNum < (time.time() - start_time) * self.fps:
                        out.write(frame)
                        frmNum += 1
                    if time.time() - start_time >= 5:
                        out.release()
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                else:
                    break
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
    cap.release()
    return ret

_record_test = False
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
        print("check if record in another process successes")
        print(canRead())
        print("end")
