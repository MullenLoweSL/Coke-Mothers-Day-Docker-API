from enum import Enum
import json
import requests
from .Singleton import Singleton

class SlackService(metaclass=Singleton):

    def __init__(self):
        pass
        
    def post_to_slack_webhook(self, text):
        # TODO: APP_SETTING
        slack_webhook_url = 'https://hooks.slack.com/services/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'
        headers = {'Content-Type': 'application/json'}
        request_body = {
            'text': text,
            'icon_emoji': ':ghost:'
        }
        
        print('Sending slack notification...')
        _ = requests.request("POST", slack_webhook_url, headers=headers, data=json.dumps(request_body))
    
    # def send_notification(self, log_level: LogLevel, text: str):
    #     # However, you can override the displayed name by sending "username": "new-bot-name" in your JSON payload. 
    #     # You can also override the bot icon either with "icon_url": "https://slack.com/img/icons/app-57.png" 
    #     # or "icon_emoji": ":ghost:".
    #     text_to_send = ''
    #     emoji = ''
    #     if log_level == LogLevel.Crash:
    #         emoji = ':collision:'
    #     elif log_level == LogLevel.Warning:
    #         emoji = ':warning:'
    #     elif log_level == LogLevel.Info:
    #         emoji = ':information_source:'
    #     elif log_level == LogLevel.Planpod:
    #         emoji = ':planpod:'
    
    #     text_to_send += emoji + ' ' + text
    #     self.post_to_slack_webhook(text=text_to_send)