import os
import json
import requests
from .Singleton import Singleton

class SunoService(metaclass=Singleton):

    def __init__(self):
        self.custom_generate_url = os.environ["SUNO_API"] + "/custom_generate"
        self.get_info = os.environ["SUNO_API"] + "/get?ids="

    def custom_generate(self, prompt, tag, title):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "prompt": prompt,
            "tags": tag,
            "title": title
        }
        response = requests.request("POST", self.custom_generate_url, headers=headers, data=json.dumps(payload))
        return response.json()

