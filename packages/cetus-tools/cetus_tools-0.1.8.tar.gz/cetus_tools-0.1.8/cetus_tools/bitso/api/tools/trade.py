def parseBitsoTrade(response):
    return {
        'book': response['book'],
        'created_at': response['created_at'],
        'amount': float(response['amount']),
        'maker_side': response['maker_side'],
        'price': float(response['price']),
        'tid': response['tid']
    }

def parseBitsoTradeArray(response):
    result = []
    for datum in response:
        result.append(parseBitsoTrade(datum))
    return result

def parseBitsoTradeDetails(response):
    return {
        'book': response['book'],
        'created_at': response['created_at'],
        'maker_side': response['maker_side'],
        'price': float(response['price']),
        'tid': response['tid'],
        'fees_amount': float(response['fees_amount']),
        'fees_currency': response['fees_currency'],
        'major': float(response['major']),
        'major_currency': response['major_currency'],
        'minor': float(response['minor']),
        'minor_currency': response['minor_currency'],
        'side': response['side'],
        'oid': response['oid']
    }

def parseBitsoTradeDetailsArray(response):
    result = []
    for datum in response:
        result.append(parseBitsoTradeDetails(datum))
    return result