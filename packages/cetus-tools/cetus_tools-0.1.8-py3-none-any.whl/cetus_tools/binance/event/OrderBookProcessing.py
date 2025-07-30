#!/usr/bin/env python
import time

def isOrderBookEvent(data):
    return ('e' in data.keys()) and (data['e'] == 'depthUpdate') and len(data['b']) > 0 and len(data['a']) > 0

def parseOrderBook(data):
    bids = parseOrderArray(data['b'])
    asks = parseOrderArray(data['a'])
    return {
        'symbol': data['s'],
        'timestamp': data['T'],
        'topBid': bids[len(bids) - 1],
        'topAsk': asks[0],
        'bids': bids,
        'asks': asks
    }

def parseOrderArray(values):
    orders = []
    for value in values:
        orders.append({
            'price': float(value[0]),
            'amount': float(value[1])
        })
    return orders

def isApiOrderBookEvent(symbol, data):
    return ('bids' in data.keys()) and ('asks' in data.keys()) and len(data['bids']) > 0 and len(data['asks']) > 0

def parseApiOrderBook(symbol, data):
    bids = parseOrderArray(data['bids'])
    asks = parseOrderArray(data['asks'])
    return {
        'symbol': symbol,
        'timestamp': time.time(),
        'topBid': bids[0],
        'secondTopBid': bids[1],
        'thirdTopBid': bids[2],
        'topAsk': asks[0],
        'bids': bids,
        'asks': asks
    }