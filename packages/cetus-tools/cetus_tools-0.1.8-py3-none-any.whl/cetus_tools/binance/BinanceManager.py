import time

from cetus_tools.binance.event.OrderBookProcessing import parseOrderArray
from cetus_tools.BrokerManager import BrokerManager

class BinanceManager(BrokerManager):
    def __init__(self, connection):
        super().__init__('binance')
        self.connection = connection
    
    def getOrderBook(self, book):
        binanceBook = self.connection.depth(book['book'], limit=10)
        return {
            'book': book['book'],
            'payload': {
                'timestamp': int(1000 * time.time()),
                'bids': parseOrderArray(binanceBook['bids']),
                'asks': parseOrderArray(binanceBook['asks']),
            }
        }
    
    def getTrades(self, book):
        result = { 'book': book['book'], 'payload': [] }
        for trade in self.connection.trades(book['book']):
            if book['lastTradeId'] < trade['id']:
                result['payload'].append({
                    'id': trade['id'],
                    'timestamp': trade['time'],
                    'price': float(trade['price']),
                    'qty': float(trade['qty']),
                    'quoteQty': float(trade['quoteQty']),
                    'isBuyerMaker': trade['isBuyerMaker'],
                    'isBestMatch': trade['isBestMatch']
                })
                book['lastTradeId'] = trade['id']
        return result
    
    def getTopPrices(self, book):
        binanceBook = self.connection.book_ticker(book['book'])
        return {
            'book': book['book'],
            'bid': float(binanceBook['bidPrice']),
            'bidSize': float(binanceBook['bidQty']),
            'ask': float(binanceBook['askPrice']),
            'askSize': float(binanceBook['askQty'])
        }
    
    def getBalances(self, book):
        return self.findBinanceBalances(book['assets'], self.connection.account()['balances'])
    
    def findBinanceBalances(self, assets, balances):
        result = {}
        for balance in balances:
            if balance['asset'].lower() in assets:
                result[balance['asset'].lower()] = {
                    'currency': balance['asset'].lower(),
                    'available': float(balance['free']),
                    'locked': float(balance['locked'])
                }
        return result
    
    def operate(self, book, side, price, quantity):
        order = self.connection.new_order(
            symbol=book['book'],
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            price=self.adjustPrice(price, book),
            quantity=self.adjustQuantity(quantity, book)
        )
        order['source'] = self.source
        order['timestamp'] = 1000 * time.time()
        order['price'] = float(order['price'])
        order['origQty'] = float(order['origQty'])
        order['executedQty'] = float(order['executedQty'])
        order['cummulativeQuoteQty'] = float(order['cummulativeQuoteQty'])
        return order
    
    def isFilledOrder(self, order):
        return order['status'] == 'FILLED'
    
    def isPartiallyFilledOrder(self, order):
        return order['status'] == 'PARTIALLY_FILLED'
    
    def isCancelledOrder(self, order):
        return order['status'] == 'CANCELED'
    
    def cancelOrder(self, order):
        self.connection.cancel_order(symbol=order['symbol'], orderId=order['orderId'])
    
    def updateOrder(self, order):
        update = self.findOrder(order)
        if update != None:
            order['status'] = update['status']
            order['executedQty'] = float(update['executedQty'])
            order['cummulativeQuoteQty'] = float(update['cummulativeQuoteQty'])
    
    def findOrder(self, order):
        return self.connection.get_order(symbol=order['symbol'], orderId=order['orderId'])
