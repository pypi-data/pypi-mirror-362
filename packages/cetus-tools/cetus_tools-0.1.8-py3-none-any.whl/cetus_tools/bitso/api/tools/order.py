def parseBitsoOrderDetails(response):
    return {
        'book': response['book'],
        'unfilled_amount': float(response['unfilled_amount']),
        'original_amount': float(response['original_amount']),
        'original_value': float(response['original_value']),
        'created_at': response['created_at'],
        'updated_at': response['updated_at'],
        'oid': response['oid'],
        'side': response['side'],
        'status': response['status'],
        'time_in_force': response['time_in_force'],
        'type': response['type'],
        'origin_id': response['origin_id'] if 'origin_id' in response.keys() else None,
        'price': float(response['price']) if 'price' in response.keys() else None,
        'stop': float(response['stop']) if 'stop' in response.keys() else None,
        'triggered_at': response['triggered_at'] if 'triggered_at' in response.keys() else None
    }

def parseBitsoOrderDetailsArray(response):
    result = []
    for datum in response:
        result.append(parseBitsoOrderDetails(datum))
    return result