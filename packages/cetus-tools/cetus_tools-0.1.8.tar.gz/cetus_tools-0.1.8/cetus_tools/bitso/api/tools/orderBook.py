def parseBitsoOrderArray(values):
    result = []
    for value in values:
        result.append({
            'book': value['book'],
            'price': float(value['price']),
            'amount': float(value['amount']),
            'oid': value['oid'] if 'oid' in value.keys() else None
        })
    return result

def parseBitsoOrderBook(response):
    return {
        'updated_at': response['updated_at'],
        'sequence': int(response['sequence']),
        'bids': parseBitsoOrderArray(response['bids']),
        'asks': parseBitsoOrderArray(response['asks'])
    }