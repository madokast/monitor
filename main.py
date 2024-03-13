import ctypes
import time

class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", ctypes.c_int32),
            ("dwHighDateTime", ctypes.c_int32)]
    def __init__(self) -> None:
        super().__init__(ctypes.c_int32(0), ctypes.c_int32(0))
    def time(self) -> int:
        t = int(self.dwHighDateTime)
        t <<= 32
        t += int(self.dwLowDateTime)
        return t
    def diffTime(self, other:'FILETIME') -> int:
        return self.time() - other.time()
    def __str__(self) -> str:
        return f"{self.dwHighDateTime}-{self.dwLowDateTime}"

class CPUMonitor:
    def __init__(self, intervalSecond:float = 1.0) -> None:
        kernel = ctypes.cdll.LoadLibrary("Kernel32.dll")
        self.GetSystemTimes = kernel.GetSystemTimes
        self.intervalSecond = intervalSecond
        self.idleTime = FILETIME()
        self.kernelTime = FILETIME()
        self.userTime = FILETIME()
        self.idleTimePtr = ctypes.pointer(self.idleTime)
        self.kernelTimePtr = ctypes.pointer(self.kernelTime)
        self.userTimePtr = ctypes.pointer(self.userTime)
        self.idleTime2 = FILETIME()
        self.kernelTime2 = FILETIME()
        self.userTime2 = FILETIME()
        self.idleTimePtr2 = ctypes.pointer(self.idleTime2)
        self.kernelTimePtr2 = ctypes.pointer(self.kernelTime2)
        self.userTimePtr2 = ctypes.pointer(self.userTime2)
    def usage(self) -> int: # percent 0-100
        while True:
            if not self.GetSystemTimes(self.idleTimePtr, self.kernelTimePtr, self.userTimePtr):
                continue
            try:
                time.sleep(self.intervalSecond)
            except:
                exit(0)
            if not self.GetSystemTimes(self.idleTimePtr2, self.kernelTimePtr2, self.userTimePtr2):
                continue
            dIdleTime = self.idleTime2.diffTime(self.idleTime)
            dKernelTime = self.kernelTime2.diffTime(self.kernelTime)
            dUserTime = self.userTime2.diffTime(self.userTime)
            totalTime = dKernelTime + dUserTime
            if totalTime <= 0:
                continue
            usage = (totalTime - dIdleTime) * 100 // totalTime
            if usage < 0 or usage > 100:
                continue
            return usage



if __name__ == "__main__":
    cm = CPUMonitor()
    while True:
        print(cm.usage())