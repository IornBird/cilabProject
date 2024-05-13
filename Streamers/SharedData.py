"""
if a video in cv2.VideoCapture modified, this capture can no longer get frame
therefore, we need a shared memory to tell that video modified
"""

import multiprocessing.managers
import numpy as np

class SharedData:
    def __init__(self, width, height):
        self._manager = multiprocessing.Manager()
        self.MODIFIED = self._manager.list()

        # for frame from stream and used by both test_5s and GUI
        self.SH_STREAM = self._manager.list()

        # for frame from output and used by both test_5s and GUI
        self.SH_RESULT = self._manager.list()
        self.rstOffset = 0

        self.ID = 0
        self.width = width
        self.height = height

    def createNew(self):
        """
        create a frame container
        :return: given ID <- remember this
        """
        with open(f"SharedFiles/{self.ID}.tmp", 'wb'):
            pass  # clear up TMP files
        self.SH_STREAM.append(None)
        self.SH_RESULT.append([])
        self.ID += 1
        return self.ID - 1

    def setStreamFrame(self, id: int, frame):
        self.SH_STREAM[id] = frame

    def getStreamFrame(self, id: int):
        return self.SH_STREAM[id]

    def addResultFrame(self, id: int, frame):
        self.SH_RESULT[id].append(frame)
        if len(self.SH_RESULT[id]) > 1024:
            with open(f"SharedFiles/RSLT{id}.tmp", 'wb') as f:
                for i in range(1024):
                    frame = self.SH_RESULT[id][0]
                    self.writeArray(frame, f)
                    self.SH_RESULT[id].pop(0)
                self.rstOffset += 1024

    def getResultFrame(self, id: int, frameNum: int) -> np.ndarray:
        """
        get [frame]-th frame since fist stored *NOT MS*
        :param frameNum: nums of frame to return
        :return: that frame
        """
        if frameNum >= self.rstOffset:
            return self.SH_RESULT[id][frameNum - self.rstOffset]

        with open(f"SharedFiles/RSLT{id}.tmp", 'rb') as f:
            f.seek(frameNum * self.height * self.width)
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


sharedData = SharedData(640, 480)
