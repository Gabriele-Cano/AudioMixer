import asyncio
from bleak import BleakClient
import threading


class BluetoothService(threading.Thread):

    connected = False
    shouldExit = False

    def __init__(self, MAC_ADDRESS, MODEL_NBR_UUID):
        super().__init__()
        self.MAC_ADDRESS = MAC_ADDRESS
        self.MODEL_NBR_UUID = MODEL_NBR_UUID
        self.data = [0, 0, 0, 0, 0]
        self.volume_data = [0, 0, 0, 0, 0]
        self.daemon = True
        self.start()

    async def notification_handler(self, sender, input_data):
        self.volume_data = list(reversed([int(self.float_map(110-input_data[0], 15, 110, 0, 100)), int(self.float_map(110-input_data[1], 15, 110, 0, 100)), int(self.float_map(110-input_data[2], 15, 110, 0, 100)), int(self.float_map(110-input_data[3], 15, 110, 0, 100)), int(self.float_map(110-input_data[4], 15, 110, 0, 100))]))
        #print(self.volume_data)

    def exit(self):
        # disconnect
        self.shouldExit = True

    def float_map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    async def main(self):
        print("main")
        async with BleakClient(self.MAC_ADDRESS) as client:
            if not client.is_connected:
                print("Failed to connect")
                return
            print(f"Connected: {client.is_connected}")
            self.connected = True
            await client.start_notify(self.MODEL_NBR_UUID, self.notification_handler)
            try:
                while not self.shouldExit:
                    await asyncio.sleep(0.1)
            except KeyboardInterrupt:
                await client.stop_notify(self.MODEL_NBR_UUID)
                print("Stopped notifications")

    def get_data(self):
        return self.volume_data

    def run(self):
        while not self.shouldExit:
            try:
                asyncio.run(self.main())
            except Exception as e:
                print(f"An error occurred: {e}")
        print("closed BluetoothService thread")