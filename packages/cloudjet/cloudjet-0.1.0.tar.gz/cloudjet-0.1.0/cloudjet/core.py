import requests

class ProxyDetection:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://apis.cloudjet.org/proxydetection.php"

    def check_ip(self, ip_address: str) -> dict:
        params = {
            "token": self.token,
            "ip": ip_address
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
