import math

class BinanceStrategyActuator:
    def __init__(self, connection, config):
        self.connection = connection
        self.config = config
    
    def canBeUsed(self, orderBook):
        pass
    
    def act(self, orderBook):
        pass
    
    def adjustPrice(self, price):
        adjustedPrice = math.floor(price / self.config['tickSize']) * self.config['tickSize']
        return round(adjustedPrice, self.config['decimals'])
    
    def adjustQuantity(self, quantity):
        return round(quantity, self.config['quantityDecimals'])
    
    def findOrder(self, orderId):
        orders = self.connection.get_all_orders(symbol=self.config['symbol'], orderId=orderId, recvWindow=2000)
        for order in orders:
            if str(order['orderId']) == str(orderId):
                return order
        return None
    
    def isFilled(self, order):
        return order['status'] == 'PARTIALLY_FILLED' or order['status'] == 'FILLED'
    
    def operate(self, side, price, quantity):
        order = self.connection.new_order(
            symbol=self.config['symbol'],
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            price=self.adjustPrice(price),
            quantity=self.adjustQuantity(quantity)
        )
        order['price'] = float(order['price'])
        order['origQty'] = float(order['origQty'])
        order['executedQty'] = float(order['executedQty'])
        order['cummulativeQuoteQty'] = float(order['cummulativeQuoteQty'])
        return order