import time

def now_ms():
    return time.time_ns() // (10 ** 6)


class TimeManager:
    def __init__(self):
        self.begin = now_ms()
        self.pause = now_ms()
        self.length = 0
        self.running = False

    def Start(self):
        """
        (re)start playing
        """
        if not self.running:
            pauseLen = now_ms() - self.pause
            self.begin += pauseLen
            self.running = True

    def Pause(self):
        """
        pause
        """
        if self.running:
            self.pause = now_ms()
            self.running = False

    def GetPalyingTime(self):
        """
        get playing time
        """
        if self.running:
            return now_ms() - self.begin
        return self.pause - self.begin

    def SetTime(self, t: int):
        """
        :param t: time you want to set on TimeManager
        """
        self.MoveTime(t - self.GetPalyingTime())

    def MoveTime(self, dt: int):
        """
        :param dt: time you want to add on TimeManger
        """
        self.begin -= dt

    def SetLength(self, t: int):
        pass