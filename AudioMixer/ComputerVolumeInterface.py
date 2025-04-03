import time
from pycaw.pycaw import *
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import math

from Interface import Interface


class ComputerVolumeInterface(Interface):

    previous_volume = 0

    def __init__(self, appName = 0, out_min=0, out_max=100):
        super().__init__(out_min, out_max)
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.sessions = AudioUtilities.GetAllSessions()
        self.appName = appName
        self.start()

    def update_value(self):
        if abs(self.value - self.previous_volume) < 5/self.out_max and self.value < 10/self.out_max:
            return
        if self.appName != 0:
            for session in self.sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == self.appName:
                    volume.SetMasterVolume(self.value / 100, None)
                    self.previous_volume = self.value
                    return
            return
        else:
            dB = 30 * math.log(self.value / 100, 10) if self.value >= 1 else -63
            self.volume.SetMasterVolumeLevel(dB, None)
            self.previous_volume = self.value
