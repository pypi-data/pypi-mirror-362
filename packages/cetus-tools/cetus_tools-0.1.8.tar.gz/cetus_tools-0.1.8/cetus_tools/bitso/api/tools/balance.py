def parseBitsoBalance(value):
    return {
        'currency': value['currency'],
        'available': float(value['available']),
        'locked': float(value['locked']),
        'total': float(value['total']),
        'pending_deposit': float(value['pending_deposit']),
        'pending_withdrawal': float(value['pending_withdrawal'])
    }

def parseBitsoBalanceArray(values):
    result = []
    for datum in values:
        result.append(parseBitsoBalance(datum))
    return result

def findBalances(currencies, balances):
    result = {}
    for balance in balances:
        if balance['currency'] in currencies:
            result[balance['currency']] = balance
    return result