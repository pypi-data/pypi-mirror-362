from cetus_tools.cetus.data.MarketDataServiceManager import MarketDataServiceManager
import requests

class BinanceMarketDataManager(MarketDataServiceManager):
    def __init__(self, url):
        super().__init__(url)
    
    def sendBook(self, book):
        response = (requests.post(self.url + '/v1/source/binance/spots', json=book)).json()
    
    def sendTrades(self, trades):
        response = (requests.post(self.url + '/v1/source/binance/trades', json=trades)).json()
    
    def getLastTrade(self, book):
        response = (requests.get(self.url + '/v1/source/binance/markets/' + book['book'] + '/trades/last')).json()
        return response['result']