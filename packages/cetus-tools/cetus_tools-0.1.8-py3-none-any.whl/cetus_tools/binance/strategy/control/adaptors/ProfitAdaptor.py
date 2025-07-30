from cetus_tools.binance.strategy.control.OrderAdaptor import OrderAdaptor

class ProfitAdaptor(OrderAdaptor):
    def init(self, order):
        order['profit']['adaptionPrice'] = order['operation']['price'] + (0.5 * (order['profit']['price'] - order['operation']['price']))
        order['profit']['adaptionSize'] = 0.6 * (order['profit']['price'] - order['operation']['price'])
        order['profit']['adaptionEnabled'] = False

    def adapt(self, orderBook, order):
        top = orderBook['topBid'] if order['operation']['side'] == 'BUY' else orderBook['topAsk']
        if top != None and self.isAdaptionEvent(top, order):
            order['profit']['adaptionEnabled'] = True
            order['profit']['adaptionPrice'] = top['price']
            return order['profit']['adaptionPrice'] - order['profit']['adaptionSize']
        return order['profit']['adaptionPrice'] - order['profit']['adaptionSize'] if order['profit']['adaptionEnabled'] == True else order['loss']['price']
    
    def isAdaptionEvent(self, top, order):
        return top['price'] > order['profit']['adaptionPrice'] if order['operation']['side'] == 'BUY' else top['price'] < order['profit']['adaptionPrice']