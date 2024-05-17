"""
if a video in cv2.VideoCapture modified, this capture can no longer get frame
therefore, we need a shared memory to tell that video modified
"""

import multiprocessing.managers
import numpy as np
import wx

from TechRecord import *

IPs = ["videos/example.mp4"] #['192.168.100.127', '192.168.100.108']
playbacks = [
            "videos/example.mp4"
            # "C:\\Users\\User\\Desktop\\source\\桂格超大便當.mp4",
            # "E:\\專題\\test.mp4",
            # "videos/0.avi",
            # "C:\\Users\\User\\Desktop\\source\\source2\\Miyabi_Love_You.mp4"
        ]

techRecord = (
            ["Yume", [TechRecord(0, Tech.KICK, Tech.TRUNK), TechRecord(2000, Tech.PUNCH, Tech.HEAD)]],
            ["Laura", [TechRecord(500, Tech.T_KICK, Tech.HEAD)]]
        )
judgeScores = ([0, 0], [0, 0])

GUIStreamer = None


class SharedData:
    def __init__(self, _manager, streamer, width, height):
        global GUIStreamer
        self.MODIFIED = _manager.list()

        # for frame from stream and used by both test_5s and GUI
        self.SH_STREAM = _manager.list()

        # for frame from output and used by both test_5s and GUI
        self.SH_RESULT = _manager.list()
        self.rstOffset = 0

        self.TMP_frame = _manager.list()

        # for ensuring all func gets same result
        self.SH_DETER = _manager.list()
        self.allPushed = _manager.list()
        self.allPushed.append(False)

        self.isWriting = _manager.list()

        self.STOP = _manager.list()
        self.STOP.append(False)

        GUIStreamer = streamer

        self.ID = 0
        self.width = width
        self.height = height

        self.flushLen = 512

    def push(self, ID, contestId, tech: TechRecord):
        if tech is None:
            self.SH_DETER[ID] = None
        else:
            self.SH_DETER[ID] = (contestId, tech)

        ref = self.SH_DETER[0]
        for c in self.SH_DETER:
            if c != ref or c is None:
                self.allPushed[0] = False
                return

        wx.CallAfter(lambda: self.allPushed.append(GUIStreamer.getTotalLength()))
        ref.time = self.allPushed[1]
        wx.CallAfter(techRecord[0][1].append(self.SH_DETER[0][1]))
        self.allPushed.pop()
        self.allPushed[0] = True

    def canResume(self):
        return self.allPushed[0]

    def createNew(self):
        """
        create a frame container
        :return: given ID <- remember this
        """
        with open(f"SharedFiles/{self.ID}.tmp", 'wb'):
            pass  # clear up TMP files
        global TMP_frame
        self.TMP_frame.append(None)
        self.SH_STREAM.append(None)
        self.SH_RESULT.append([])
        self.SH_DETER.append(None)
        self.isWriting.append(False)

        self.ID += 1
        return self.ID - 1

    def setStreamFrame(self, id: int, frame):
        self.SH_STREAM[id] = frame

    def getStreamFrame(self, id: int):
        return self.SH_STREAM[id]

    def addResultFrame(self, id: int, frame):
        self.SH_RESULT[id].append(frame)
        if len(self.SH_RESULT[id]) > self.flushLen:
            with open(f"SharedFiles/RSLT{id}.tmp", 'ab') as f:
                for i in range(self.flushLen):
                    frame = self.SH_RESULT[id][0]
                    self.writeArray(frame, f)
                    self.SH_RESULT[id].pop(0)
                    self.rstOffset += 1

    def getResultFrame(self, id: int, frameNum: int) -> np.ndarray | None:
        """
        get [frame]-th frame since fist stored *NOT MS*
        :param frameNum: nums of frame to return
        :return: that frame
        """
        while self.isWriting[id]:
            pass
        if frameNum >= self.rstOffset + len(self.SH_RESULT[id]):
            return None
        elif frameNum >= self.rstOffset:
            return self.SH_RESULT[id][frameNum - self.rstOffset]

        with open(f"SharedFiles/RSLT{id}.tmp", 'rb') as f:
            f.seek(frameNum * self.height * self.width, 0)
            frame = f.read(3 * self.height * self.width)

            ans = np.empty((self.height, self.width, 3))
            RGB = 0
            PT = 0
            LINE = 0
            for c in frame:
                ans[LINE][PT][RGB] = c
                RGB += 1
                if RGB == 3:
                    RGB = 0
                    PT += 1
                if PT == self.width:
                    PT = 0
                    LINE += 1
            return ans

    def writeArray(self, frame, f):
        # format: ndarray: (height, width, 3)
        for line in frame:
            for pixel in line:
                f.write(bytes(pixel))

