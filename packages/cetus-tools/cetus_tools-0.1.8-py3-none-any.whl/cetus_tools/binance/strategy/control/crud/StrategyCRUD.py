import requests

def findOrCreateStrategy(strategyCrudUrl, definition):
    response = (requests.get(strategyCrudUrl + '/v1/strategies?name=' + definition['name'] + '&tag=' + definition['tag'])).json()
    if len(response['result']) == 0:
        response = (requests.post(strategyCrudUrl + '/v1/strategies', json=definition)).json()
        return response['items'][0]
    return response['result'][0]

def findStrategyRequests(strategyCrudUrl, strategyId):
    try:
        response = (requests.get(strategyCrudUrl + '/v1/requests?strategyId=' + str(strategyId) + '&status=SUBMITTED,PLACED,FILLED,FORCED_CLOSING')).json()
        return response['result']
    except:
        return []

def updateStrategyRequest(strategyCrudUrl, definition):
    response = requests.put(strategyCrudUrl + '/v1/requests/' + str(definition['strategyRequestId']), json={
        'status': definition['status'],
        'details': definition['details']
    })

def updateStrategy(strategyCrudUrl, definition):
    response = requests.put(strategyCrudUrl + '/v1/strategies/' + str(definition['strategyId']), json={
        'config': definition['config'],
        'memory': definition['memory']
    })