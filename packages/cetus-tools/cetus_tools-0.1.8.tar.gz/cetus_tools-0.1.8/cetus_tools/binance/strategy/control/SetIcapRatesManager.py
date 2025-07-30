import datetime
import math
import time

class SetIcapRatesManager:
    def __init__(self, apiManager):
        self.apiManager = apiManager
    
    def getSetIcapRate(self, prices):
        if self.isWorkingHours():
            rates = self.apiManager.getRates()
            for rate in rates:
                if self.isValidRate(rate):
                    return self.buildRatePrices(rate, prices)
        return None
    
    def isValidRate(self, rate):
        return (rate['symbol'] == 'USDCOP') and (rate['source'] == 'CMA') and('bid' in rate.keys()) and ('ask' in rate.keys())
    
    def isWorkingHours(self):
        date = datetime.datetime.now(datetime.timezone.utc)
        return date.hour >= 13 and date.hour < 22 and date.weekday() < 5 
    
    def buildRatePrices(self, rate, prices):
        rate['timestamp'] = math.floor(1000 * time.time())
        for price in prices:
            if price['key'] in rate.keys():
                rate[price['name']] = max(rate[price['key']] - price['spread'], 0)
        return rate