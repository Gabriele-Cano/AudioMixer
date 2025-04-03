import threading
import time
import atexit
import pystray
from PIL import Image

from HomeAssistantInterface import HomeAssistantInterface
from BluetoothService import BluetoothService
from BrightnessInterface import BrightnessInterface
from ComputerVolumeInterface import ComputerVolumeInterface

HOME_ASSISTANT_TOKEN = ""
HOME_ASSISTANT_URL = ""
MAC_ADDRESS = "C0:4E:30:81:E0:9E"
MODEL_NBR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

main = None


class Main(threading.Thread):
    shouldExit = False

    def __init__(self):
        super().__init__()
        atexit.register(exit)
        self.bluetooth_service = BluetoothService(MAC_ADDRESS, MODEL_NBR_UUID)
        self.threads = [
            (ComputerVolumeInterface()),
            (ComputerVolumeInterface("WsaClient.exe", 0, 10)),
            (ComputerVolumeInterface("chrome.exe")),
            (ComputerVolumeInterface("Discord.exe")),
            (BrightnessInterface(0, 50, 3)),
            #(HomeAssistantInterface(HOME_ASSISTANT_TOKEN, HOME_ASSISTANT_URL, ["media_player.samsung_6_series_43", "media_player"], 0, 20)),
        ]
        self.start()

    def exit(self):
        print("exit...")
        self.bluetooth_service.exit()
        self.bluetooth_service.join()
        self.shouldExit = True

    def run(self):
        while not self.shouldExit:
            if not self.bluetooth_service.connected:
                time.sleep(.01)
                continue
            data = self.bluetooth_service.get_data()
            for i in range(len(self.threads)):
                self.threads[i].set_value(data[i])
            time.sleep(.01)
        print("Closed Main thread")


def after_click(icon, item):
    if item.text == "Exit":
        main.exit()
        icon.stop()
    else:
        print(item.text)


if __name__ == "__main__":
    main = Main()
    image = Image.open("icon.png")
    icon = pystray.Icon("Audio Mixer", image, "Audio Mixer", menu=pystray.Menu(
        pystray.MenuItem("Exit", after_click)))
    icon.run()
