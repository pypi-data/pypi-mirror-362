import requests

class SecureSpeakClient:
    BASE_URL = "https://securespeak-api-1064980124131.us-central1.run.app"

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def analyze_file(self, file_path):
        """Analyze uploaded audio file"""
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{self.BASE_URL}/analyze_file",
                headers=self.headers,
                files={"file": f}
            )
        response.raise_for_status()
        return response.json()

    def analyze_url(self, url):
        """Analyze audio from URL"""
        response = requests.post(
            f"{self.BASE_URL}/analyze_url",
            headers=self.headers | {"Content-Type": "application/json"},
            json={"url": url}
        )
        response.raise_for_status()
        return response.json()

    def analyze_live(self, file_path):
        """Analyze live audio (per-second billing)"""
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{self.BASE_URL}/analyze_live",
                headers=self.headers,
                files={"file": f}
            )
        response.raise_for_status()
        return response.json() 