from cetus_tools.binance.strategy.control.OrderAdaptor import OrderAdaptor

class LossAdaptor(OrderAdaptor):
    def init(self, order):
        order['loss']['adaptionPrice'] = order['operation']['price'] - (0.5 * (order['operation']['price'] - order['loss']['price']))
        order['loss']['adaptionSize'] = 0.6 * (order['operation']['price'] - order['loss']['price'])
        order['loss']['adaptionEnabled'] = False

    def adapt(self, orderBook, order):
        top = orderBook['topBid'] if order['operation']['side'] == 'BUY' else orderBook['topAsk']
        if top != None:
            if order['loss']['adaptionEnabled'] == False:
                order['loss']['adaptionEnabled'] = top['price'] < order['loss']['adaptionPrice'] if order['operation']['side'] == 'BUY' else top['price'] > order['loss']['adaptionPrice']
            elif self.isAdaptionEvent(top, order):
                order['loss']['adaptionPrice'] = top['price']
                return order['loss']['adaptionPrice'] - order['loss']['adaptionSize']
        return order['loss']['adaptionPrice'] - order['loss']['adaptionSize'] if order['loss']['adaptionEnabled'] == True else order['loss']['price']
    
    def isAdaptionEvent(self, top, order):
        return top['price'] > order['loss']['adaptionPrice'] if order['operation']['side'] == 'BUY' else top['price'] < order['loss']['adaptionPrice']