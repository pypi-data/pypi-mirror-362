import math

class BrokerManager:
    def __init__(self, source):
        self.source = source

    def getOrderBook(self, book):
        pass

    def getTopPrices(self, connection, book):
        pass
    
    def getBalances(self, book):
        pass
    
    def operate(self, book, side, price, quantity):
        pass
    
    def isFilledOrder(self, order):
        pass
    
    def isPartiallyFilledOrder(self, order):
        pass
    
    def isCancelledOrder(self, order):
        pass
    
    def cancelOrder(self, order):
        pass
    
    def updateOrder(self, order):
        pass
    
    def findOrder(self, order):
        pass
    
    def adjustPrice(self, price, book):
        adjustedPrice = math.floor(price / book['tickSize']) * book['tickSize']
        return round(adjustedPrice, book['decimals'])
    
    def adjustQuantity(self, quantity, book):
        return round(quantity, book['quantityDecimals'])