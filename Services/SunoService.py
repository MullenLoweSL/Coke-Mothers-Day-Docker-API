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
        response_json = response.json()
        # response JSON always has 2 entries, take 1st one (arbitrarily)
        return response_json[0]['id']

