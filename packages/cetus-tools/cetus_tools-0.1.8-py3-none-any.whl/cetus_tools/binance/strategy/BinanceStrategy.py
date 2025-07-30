class BinanceStrategy:
    def __init__(self, connection, logger, config):
        self.connection = connection
        self.logger = logger
        self.config = config
    
    def init(self, symbol):
        pass
    
    def apply(self, orderBook):
        pass