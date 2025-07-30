import time
import requests

from cetus_tools.BrokerManager import BrokerManager
from cetus_tools.bitso.api.tools.book import findBitsoBook
from cetus_tools.bitso.api.tools.balance import findBalances

class BitsoManager(BrokerManager):
    def __init__(self, connection):
        super().__init__('bitso')
        self.connection = connection
    
    def getOrderBook(self, book):
        pass
    
    def getTopPrices(self, book):
        books = findBitsoBook([book['book']], self.connection.getAvailableBookList())
        orderBook = self.connection.getOrderBook(books[book['book']], None)
        return {
            'book': book['book'],
            'bid': orderBook['bids'][0]['price'],
            'bidSize': orderBook['bids'][0]['amount'],
            'ask': orderBook['asks'][0]['price'],
            'askSize': orderBook['asks'][0]['amount']
        }
    
    def getBalances(self, book):
        return findBalances(book['assets'], self.connection.getBalances())
    
    def operate(self, book, side, price, quantity):
        order = self.connection.placeOrder({
            'timestamp': 1000 * time.time(),
            'book': book['book'],
            'side': side,
            'type': 'limit',
            'status': 'placed',
            'price': self.adjustPrice(price, book),
            'major': self.adjustQuantity(quantity, book)
        })
        if order != None and 'oid' in order.keys():
            order = self.connection.lookUpOrder(order['oid'])[0]
            order['symbol'] = book['book']
            order['orderId'] = order['oid']
            order['timestamp'] = 1000 * time.time()
            order['source'] = self.source
            order['origQty'] = order['original_amount']
            order['executedQty'] = order['original_amount'] - order['unfilled_amount']
            order['cummulativeQuoteQty'] = order['price'] * order['executedQty']
            return order
        return None
    
    def isFilledOrder(self, order):
        return order['status'] == 'completed'
    
    def isPartiallyFilledOrder(self, order):
        return order['status'] == 'partially filled'
    
    def isCancelledOrder(self, order):
        return order['status'] == 'cancelled'
    
    def cancelOrder(self, order):
        return self.connection.cancelOrder(order['oid'])
    
    def findOrder(self, order):
        return self.connection.lookUpOrder(order['oid'])
    
    def updateOrder(self, order):
        update = self.connection.lookUpOrder(order['oid'])[0] if 'oid' in order.keys() else None
        if update != None:
            order['unfilled_amount'] = update['unfilled_amount']
            order['status'] = update['status']
            order['executedQty'] = update['original_amount'] - update['unfilled_amount']
            order['cummulativeQuoteQty'] = order['price'] * order['executedQty']