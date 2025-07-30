import math
import requests
from datetime import datetime

class LogManager:
    def __init__(self, url):
        self.url = url
    
    def register(self, strategyId, details):
        response = (requests.post(self.url + '/v1/executions', json={
            'timestamp': math.floor(1000 * datetime.timestamp(datetime.now())),
            'strategyId': strategyId,
            'details': details
        })).json()
        return response['payload']['executionId']
    
    def sendExecutionLog(self, executionId, action, details):
        return (requests.post(self.url + '/v1/executions/' + executionId + '/logs', json={
            'timestamp': math.floor(1000 * datetime.timestamp(datetime.now())),
            'action': action,
            'details': details
        })).json()