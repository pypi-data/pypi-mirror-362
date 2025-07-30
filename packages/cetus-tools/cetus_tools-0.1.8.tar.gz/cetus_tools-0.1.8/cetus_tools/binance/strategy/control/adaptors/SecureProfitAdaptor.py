from cetus_tools.binance.strategy.control.OrderAdaptor import OrderAdaptor

class SecureProfitAdaptor(OrderAdaptor):
    def init(self, order):
        order['profit']['securityPrice'] = order['operation']['price'] + (0.95 * (order['profit']['price'] - order['operation']['price']))
        order['profit']['securitySize'] = 0.05 * (order['profit']['price'] - order['operation']['price'])
        order['profit']['securityEnabled'] = False

    def adapt(self, orderBook, order):
        top = orderBook['topBid'] if order['operation']['side'] == 'BUY' else orderBook['topAsk']
        if top != None and self.isAdaptionEvent(top, order):
            order['profit']['securityEnabled'] = True
            order['profit']['securityPrice'] = top['price']
            return order['profit']['securityPrice'] - order['profit']['securitySize']
        return order['profit']['securityPrice'] if order['profit']['securityEnabled'] == True else order['loss']['price']
    
    def isAdaptionEvent(self, top, order):
        return top['price'] > order['profit']['securityPrice'] if order['operation']['side'] == 'BUY' else top['price'] < order['profit']['securityPrice']