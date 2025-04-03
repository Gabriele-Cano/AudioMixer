import threading
import time


class Interface(threading.Thread):
    def __init__(self, out_min, out_max):
        super().__init__()
        self.out_min = out_min
        self.out_max = out_max
        self.shouldExit = False
        self.daemon = True
        self.value = None

    def exit(self):
        self.shouldExit = True

    def update_value(self):
        pass

    def set_value(self, value):
        self.value = int(self.map(value))

    def map(self, x):
        return x * (self.out_max - self.out_min) / 100 + self.out_min

    def run(self):
        while not self.shouldExit:
            time.sleep(.01)
            if self.value is not None: self.update_value()
        print(f"Closed {type(self).__name__} thread")