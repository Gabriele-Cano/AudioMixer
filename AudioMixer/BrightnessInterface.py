import datetime

import screen_brightness_control as sbc
import time

from Interface import Interface


class BrightnessInterface(Interface):

    previous_brightness = 0

    def __init__(self, out_min=0, out_max=100, tolerance=5):
        super().__init__(out_min, out_max)
        self.tolerance = tolerance
        self.shouldExit = False
        self.start()

    def update_value(self):
        if abs(self.value - self.previous_brightness) < self.tolerance:
            return
        print(datetime.datetime.now(), self.value, self.previous_brightness)
        sbc.fade_brightness(self.value)
        time.sleep(0.1)
        self.previous_brightness = sbc.get_brightness()[0]