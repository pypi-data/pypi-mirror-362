from cetus_tools.binance.strategy.control.OrderAdaptor import OrderAdaptor

class ForceClosingAdaptor(OrderAdaptor):
    def init(self, order):
        order['loss']['forceClosingSize'] = 0.05 * (order['profit']['price'] - order['operation']['price'])
        order['loss']['forceClosingEnabled'] = False

    def adapt(self, orderBook, order):
        top = orderBook['topBid'] if order['operation']['side'] == 'BUY' else orderBook['topAsk']
        return top['price'] - order['loss']['forceClosingSize'] if top != None and order['loss']['forceClosingEnabled'] == True else order['loss']['price']