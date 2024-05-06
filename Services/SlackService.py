import os
import json
import requests
from .Singleton import Singleton

class SlackService(metaclass=Singleton):

    def __init__(self):
        self.slack_webhook_url = os.environ["WEBOOK_SLACK"]
        
    def post_to_slack_webhook(self, text):
        # TODO: APP_SETTING
        headers = {'Content-Type': 'application/json'}
        request_body = {
            'text': text,
            'icon_emoji': ':ghost:'
        }
        
        print('Sending slack notification...')
        _ = requests.request("POST", self.slack_webhook_url, headers=headers, data=json.dumps(request_body))