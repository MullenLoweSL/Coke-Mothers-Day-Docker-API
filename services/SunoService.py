import os
import json
import requests
from .Singleton import Singleton

class SunoService(metaclass=Singleton):

    def __init__(self):
        self.custom_generate_url = os.environ["SUNO_API"] + "/custom_generate"
        self.ai_generate_url = os.environ["SUNO_API"] + "/generate"
        self.get_info = os.environ["SUNO_API"] + "/get?ids="

    def custom_generate(self, prompt, tag, title):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "prompt": prompt,
            "tags": tag,
            "title": title,
            "make_instrumental": False
        }
        response = requests.request("POST", self.custom_generate_url, headers=headers, data=json.dumps(payload))
        response_json = response.json()
        # response JSON always has 2 entries, take 1st one (arbitrarily)
        return response_json[0]['id']

    def ai_generate(self, prompt):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "prompt": prompt,
            "make_instrumental": False,
            "wait_audio": False
        }
        response = requests.request("POST", self.ai_generate_url, headers=headers, data=json.dumps(payload))
        response_json = response.json()
        # response JSON always has 2 entries, take 1st one (arbitrarily)
        return response_json[0]['id']

    def get_song_URL(self, suno_song_id):
        headers = {'Content-Type': 'application/json'}
        response = requests.request("GET", self.get_info + suno_song_id, headers=headers)
        response_json = response.json()
        if response_json[0]['audio_url']:
            return response_json[0]['audio_url']
        return None

