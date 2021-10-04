import json

def close_response(intent_request, intent_name):
    
    resp = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "confirmationState": "Confirmed",
                "name": intent_name,
                "state": "Fulfilled",
            },
    
        },
        
    }
    
    return resp

    
    
def intent_handler(intent_request):
    print('result: ')
    print(intent_request)
    print('after: ')
    
    intent_name = intent_request['sessionState']['intent']['name']
    
    if intent_name == 'GreetingIntent':
        return close_response(intent_request, intent_name)
    else:
        return None
        
        



def lambda_handler(event, context):
    # TODO implement
    return intent_handler(event)