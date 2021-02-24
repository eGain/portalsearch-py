import http.client
import json
#import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

token = ""
portalid = "555500000001000"

def anonyomous_access():
    # TODO implement
    global token
    connection = http.client.HTTPSConnection('ecosystem.egain.cloud')
    headers = {'Accept': 'application/json','Accept-Language': 'en-US'}
    connection.request('POST', '/system/ws/v15/ss/portal/'+portalid+'/authentication/anonymous',"",headers)
    response = connection.getresponse()
    status = response.status
    token = response.getheader('X-egain-session')
    print ("anonymous access status", status, "token", token)    
    return status

def search():
    # TODO implement
    connection = http.client.HTTPSConnection('ecosystem.egain.cloud')
    headers = {'Content-Type': 'application/json','Accept': 'application/json','Accept-Language': 'en-US','X-egain-session': token}
    connection.request('GET', '/system/ws/v11/ss/search?portalId='+portalid+'&q=eGain&rangestart=0&rangesize=5&usertype=customer&$attribute=all',"",headers)
    response = connection.getresponse()
    status = response.status 
    print ("search status", status) 
    if (status == 200):
        return response.read()
    else:
        return null

def dispatch(event):
    """
    Called when the user specifies an intent for this bot.
    """

    # Dispatch to your bot's intent handlers
    if (event['currentIntent']['name'] == 'Search'):
        status = anonyomous_access()
        response = '{"sessionAttributes": { },"dialogAction": {"type": "Close","fulfillmentState": "Fulfilled","message": {"contentType": "PlainText","content": ""}}}'
        jsonresponse = json.loads(response)
        result = search()
        if (result != '') :
            data = json.loads(result)
            links = ""
            for article in data['article']:
                links += article['link']['href']+'\n'		
            logger.debug('status:{} search {}'.format(status, "Search"))
            jsonresponse["dialogAction"]["message"]["content"] = links
            return jsonresponse
        else:		
            logger.debug('status {}',format(status))
            jsonresponse["message"]["content"] = "Search is down"
            return jsonresponse
    raise Exception('Intent with name ' + intent_name + ' not supported')
    
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    logger.debug(format(event))
    return dispatch(event)

