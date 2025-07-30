import threading
import time
import requests
from .config import CODEW_API_URL


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class KXYState:

    def __init__(self):
        self.enabled_kxy = "not_initialized"
        self.performance_enabled = False
        self.memory_enabled = False
        self.logging_enabled = False
        self.token_secret = ""
        self.codew_api = CODEW_API_URL
        threading.Thread(target=self.loop, daemon=True).start()

    def get_secret(self):
        return self.token_secret

    def set_secret(self, secret):
        self.token_secret = secret
        self.check_token()

    def loop(self):
        while True:
            if not self.token_secret:
                time.sleep(0.5)
                continue
            self.check_token()
            time.sleep(2)

    def check_token(self):
        if self.enabled_kxy != "not_initialized":
            return

        base_url = self.codew_api + "/kxy/status"
        try:
            response = requests.post(base_url, headers={"secret": self.token_secret}, timeout=2)
            response.raise_for_status()
            self.enabled_kxy = response.text.strip()
            if self.enabled_kxy == "1":
                self.performance_enabled = True

        except Exception as e:
            print("Error checking KXY status:", e)

    def parse_app_config(self):
        ...
