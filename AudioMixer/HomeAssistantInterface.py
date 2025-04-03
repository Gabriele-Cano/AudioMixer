import time
import requests
from Interface import Interface


class HomeAssistantInterface(Interface):

    previous_volume = 0

    def __init__(self, HOME_ASSISTANT_TOKEN, HOME_ASSISTANT_URL, device, out_min=0, out_max=100):
        super().__init__(out_min, out_max)
        self.HOME_ASSISTANT_TOKEN = HOME_ASSISTANT_TOKEN
        self.HOME_ASSISTANT_URL = HOME_ASSISTANT_URL
        self.device = device
        self.headers = {
            "Authorization": "Bearer " + self.HOME_ASSISTANT_TOKEN,
            "content-type": "application/json",
        }
        self.start()

    def get_volume(self):
        response = requests.get(self.HOME_ASSISTANT_URL + "states/" + self.device[0],
                                headers=self.headers).json()
        return int(response.get("attributes").get("volume_level") * 100) if response.get("state") != "off" else -1

    def update_value(self):
        if self.value is not None:
            if self.device[1] == "webostv":
                self.set_webos_volume(self.value)
            elif self.device[1] == "media_player":
                self.set_media_player_volume(self.value)

    def set_webos_volume(self, volume, ):
        deltaVolume = volume - self.get_volume()
        if abs(deltaVolume) < 1: return
        if deltaVolume > 0:
            button = "VOLUMEUP"
        else:
            button = "VOLUMEDOWN"
        for i in range(abs(deltaVolume)):
            requests.post(self.HOME_ASSISTANT_URL + "services/webostv/button", headers=self.headers,
                          json={"entity_id": self.device[0], "button": button})
            time.sleep(0.05)

    def set_media_player_volume(self, volume):
        if abs(volume - self.previous_volume) < 1: return
        requests.post(self.HOME_ASSISTANT_URL + "services/media_player/volume_set", headers=self.headers,
                      json={"entity_id": self.device[0], "volume_level": volume / 100})
        self.previous_volume = volume