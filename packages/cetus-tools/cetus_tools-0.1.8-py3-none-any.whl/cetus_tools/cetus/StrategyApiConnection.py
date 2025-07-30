import requests
import hashlib
import json
import math
import time
import hmac

def convert_float_like_integers(data):
    if isinstance(data, dict):
        return {k: convert_float_like_integers(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_float_like_integers(item) for item in data]
    elif isinstance(data, float) and data.is_integer():
        return int(data)
    else:
        return data

class StrategyApiManager:
    def __init__(self, keys, apiUrl):
        self.apiUrl = apiUrl
        self.keys = keys
    
    def sign(self, method, path, body):
        nonce = math.floor(1000 * time.time())
        message = str(nonce) + method + path.replace(" ", "%20") + json.dumps(convert_float_like_integers(body), separators=(',', ':'))
        signature = hmac.new(bytes(self.keys['secretKey'], 'utf-8'), msg=bytes(message, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
        return { "Authorization": "cetus " + self.keys['publicKey'] + ":" + str(nonce) + ":" + signature }
    
    def getStrategies(self, name, pair, account):
        url = "/v1/strategies?name=" + name + "&pair=" + pair + "&account=" + account
        signature = self.sign("GET", url, {})
        return (requests.get(self.apiUrl + url, headers=signature)).json()['result']
    
    def updateStrategy(self, strategy):
        url = "/v1/strategies/" + str(strategy['id'])
        payload = { 'memory': strategy['memory'] }
        signature = self.sign("PUT", url, payload)
        return requests.put(self.apiUrl + url, headers=signature, json=payload).json()
    
    def getWallets(self, address, network):
        url = "/v1/kyc/wallets?address=" + address + "&network=" + network
        signature = self.sign("GET", url, {})
        return requests.get(self.apiUrl + url, headers=signature).json()['result']
    
    def createWallet(self, address, network):
        url = "/v1/kyc/wallets"
        payload = { 'address': address, 'network': network }
        signature = self.sign("POST", url, payload)
        return requests.post(self.apiUrl + url, headers=signature, json=payload).json()
    
    def createWalletActivity(self, walletId, activityType, details):
        url = "/v1/kyc/activities"
        payload = { 'walletId': walletId, 'type': activityType, 'details': details, 'timestamp': math.floor(1000 * time.time()) }
        signature = self.sign("POST", url, payload)
        return requests.post(self.apiUrl + url, headers=signature, json=payload).json()
    
    def getRates(self):
        url = "/v1/rates"
        signature = self.sign("GET", url, {})
        return (requests.get(self.apiUrl + url, headers=signature)).json()['rates']
    
    def createOrder(self, strategyId, order):
        url = "/v1/strategies/orders"
        payload = { 'strategyId': strategyId, 'order': order }
        signature = self.sign("POST", url, payload)
        return requests.post(self.apiUrl + url, headers=signature, json=payload).json()