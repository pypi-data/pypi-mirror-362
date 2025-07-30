import requests
import urllib.parse

class TelegramChannelManager:
    def __init__(self, url, config):
        self.url = url
        self.config = config
    
    def sendText(self, content):
        try:
            url = self.url + '/bot' + self.config['token'] + '/sendMessage?chat_id=' + self.config['channelId']
            response = requests.get(url + '&text=' + urllib.parse.quote(content.encode('utf-8')))
        except:
            print("> Telegram message could not be sent")