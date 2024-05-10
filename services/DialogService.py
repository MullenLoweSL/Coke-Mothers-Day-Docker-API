import os
import json
import requests
from .Singleton import Singleton
from datetime import datetime, timedelta

class DialogService(metaclass=Singleton):

    def __init__(self):
        self.username = os.environ["DIALOG_USERNAME"]
        self.password = os.environ["DIALOG_PASSWORD"]
        self.access_token = None
        self.token_expiry = datetime.utcnow()

    def get_access_token(self):
        if self.access_token and self.token_expiry > datetime.utcnow():
            return self.access_token

        # Your code to generate a new access token goes here
        self.access_token = self.generate_new_access_token()

        # Set the expiry time for the token to 6 hours from now
        self.token_expiry = datetime.utcnow() + timedelta(hours=6)

        return self.access_token
    
    def generate_new_access_token(self):
        url = "https://digitalreachapi.dialog.lk/refresh_token.php"
        payload = json.dumps({
            "u_name": self.username,
            "passwd": self.password
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = response.json()
        token = response_json['access_token']
        return token

    def send_sms(self, message, recipient):
        url = "https://digitalreachapi.dialog.lk/camp_req.php"
        access_token = self.get_access_token()

        payload = json.dumps({
            "msisdn": recipient,
            "channel": "1",
            "mt_port": "COCA COLA",
            "s_time": "2024-05-07 08:00:00",
            "e_time": "2024-06-14 16:00:00",
            "msg": message,
            "callback_url": "http://www.youreurl.com"
        })
        headers = {
            'Authorization': str(access_token),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = response.json()
        result = response_json['error']
        if result == "0":
            return True
        return False