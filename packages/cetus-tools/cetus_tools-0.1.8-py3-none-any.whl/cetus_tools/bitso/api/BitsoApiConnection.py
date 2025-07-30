import time
import hmac
import json
import hashlib
import requests

from cetus_tools.bitso.api.tools.book import parseBitsoBookArray
from cetus_tools.bitso.api.tools.trade import parseBitsoTradeArray
from cetus_tools.bitso.api.tools.orderBook import parseBitsoOrderBook
from cetus_tools.bitso.api.tools.balance import parseBitsoBalanceArray
from cetus_tools.bitso.api.tools.order import parseBitsoOrderDetailsArray
from cetus_tools.bitso.api.tools.trade import parseBitsoTradeDetailsArray

class BitsoApiConnection:
    def __init__(self, config):
        self.config = config
    
    def sign(self, method, path, body):
        nonce = int(time.time() * 1000)
        message = bytes(str(nonce) + method + path + (json.dumps(body) if body != None else ""), 'utf-8')
        signature = hmac.new(self.config['apiSecret'], msg=message, digestmod=hashlib.sha256).hexdigest()
        return { 'Authorization': 'Bitso ' +  self.config['apiKey'] + ':' + str(nonce) + ':' + signature }
    
    def getBalances(self):
        signature = self.sign('GET', '/api/v3/balance/', None)
        response = requests.get(self.config['url'] + '/api/v3/balance/', headers=signature).json()
        return parseBitsoBalanceArray(response['payload']['balances'])
    
    def getAvailableBookList(self):
        signature = self.sign('GET', '/api/v3/available_books/', None)
        response = requests.get(self.config['url'] + '/api/v3/available_books/', headers=signature).json()
        return parseBitsoBookArray(response['payload'])
    
    def getOrderBook(self, book, aggregate):
        url = '/api/v3/order_book/?book=' + book['book'] + '&aggregate=' + str(aggregate if aggregate != None else True)
        signature = self.sign('GET', url, None)
        response = requests.get(self.config['url'] + url, headers=signature).json()
        return parseBitsoOrderBook(response['payload'])
    
    def placeOrder(self, body):
        signature = self.sign('POST', '/api/v3/orders/', body)
        response = requests.post(self.config['url'] + '/api/v3/orders/', json=body, headers=signature).json()
        return response['payload'] if response['success'] else None
    
    def lookUpOrder(self, oid):
        url = '/api/v3/orders/' + oid + '/'
        signature = self.sign('GET', url, None)
        response = requests.get(self.config['url'] + url, headers=signature).json()
        return parseBitsoOrderDetailsArray(response['payload']) if response['success'] else []
    
    def getUserOpenOrders(self, book):
        url = '/api/v3/open_orders/?book=' + book['book']
        signature = self.sign('GET', url, None)
        response = requests.get(self.config['url'] + url, headers=signature).json()
        return parseBitsoOrderDetailsArray(response['payload']) if response['success'] else []
    
    def cancelOrder(self, oid):
        url = '/api/v3/orders/' + oid + '/'
        signature = self.sign('DELETE', url, None)
        response = requests.delete(self.config['url'] + url, headers=signature).json()
        return response['payload'] if response['success'] else []
    
    def getTrades(self, book):
        url = '/api/v3/trades/?book=' + book['book'] + ('&limit=' + str(book['limit']) if 'limit' in book.keys() else '') + ('&maker=' + str(book['maker']) if 'maker' in book.keys() else '') + ('&sort=' + str(book['sort']) if 'sort' in book.keys() else '')
        signature = self.sign('GET', url, None)
        response = requests.get(self.config['url'] + url, headers=signature).json()
        return parseBitsoTradeArray(response['payload']) if response['success'] else []
    
    def getOrderTrades(self, oid):
        try:
            url = '/api/v3/order_trades/' + oid + '/'
            signature = self.sign('DELETE', url, None)
            response = requests.delete(self.config['url'] + url, headers=signature).json()
            return parseBitsoTradeDetailsArray(response['payload']) if response['success'] else []
        except:
            print("> error getting trades")
            return []

    def getFees(self):
        signature = self.sign('GET', '/api/v3/fees/', None)
        response = requests.get(self.config['url'] + '/api/v3/fees/', headers=signature).json()
        return response
    
    def getTicker(self, book):
        url = '/api/v3/ticker/?book=' + book['book']
        signature = self.sign('GET', url, None)
        response = requests.get(self.config['url'] + url, headers=signature).json()
        return response