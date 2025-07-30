def calculateDecimals(tickSize):
    cnt = 0
    while tickSize < 1:
        tickSize *= 10
        cnt = cnt +1
    return cnt

def parseBitsoBookFeesRate(response):
    return {
        'maker': float(response['maker']),
        'taker': float(response['taker']),
        'volume': float(response['maker']) if 'volume' in response.keys() else None
    }

def parseBitsoBookFeesRateArray(response):
    result = []
    for value in response:
        result.append(parseBitsoBookFeesRate(value))
    return result

def parseBitsoBook(response):
    return {
        'book': response['book'],
        'default_chart': response['default_chart'],
        'minimum_price': float(response['minimum_price']),
        'maximum_price': float(response['maximum_price']),
        'minimum_value': float(response['minimum_value']),
        'maximum_value': float(response['maximum_value']),
        'minimum_amount': float(response['minimum_amount']),
        'maximum_amount': float(response['maximum_amount']),
        'tick_size': float(response['tick_size']),
        'decimals': calculateDecimals(float(response['tick_size'])),
        'fees': {
            'flat_rate': parseBitsoBookFeesRate(response['fees']['flat_rate']),
            'structure': parseBitsoBookFeesRateArray(response['fees']['structure'])
        }
    }

def parseBitsoBookArray(response):
    result = []
    for datum in response:
        result.append(parseBitsoBook(datum))
    return result

def findBitsoBook(pairs, books):
    result = {}
    for book in books:
        if book['book'] in pairs:
            result[book['book']] = book
    return result