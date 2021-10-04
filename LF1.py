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


def ds_response(intent_request, intent_name):
    invocation_source = intent_request['invocationSource']
    if invocation_source == 'DialogCodeHook':
        slots = intent_request['sessionState']['intent']['slots']
        
        #here we should validate if slots are valid

        resp = {
            "sessionState": {
                "dialogAction": {
                    "type": 'Delegate'
                },
                "intent": {
                    "confirmationState": 'None',
                    "name": intent_name,
                    "state": 'InProgress',
                    "slots": slots,
                },
            },        
        }
    
        return resp

    else:
        #FulfillmentCodeHook
        return close_response(intent_request, intent_name)

    
    
def intent_handler(intent_request):
    print('result: ')
    print(intent_request)
    print('after: ')
    
    intent_name = intent_request['sessionState']['intent']['name']
    
    if intent_name == 'GreetingIntent':
        return close_response(intent_request, intent_name)
    elif intent_name == 'DiningSuggestionsIntent':
        return ds_response(intent_request, intent_name)
    else:
        return None
        
        



def lambda_handler(event, context):
    # TODO implement
    return intent_handler(event)