import json
import boto3

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

def get_slot(slot):
    if slot is not None:
        if 'interpretedValue' in slot['value']:
            return slot['value']['interpretedValue']
        else:
            return slot['value']['originalValue']
    else:
        return None



def ds_response(intent_request, intent_name):
    #get slots
    slots = intent_request['sessionState']['intent']['slots']
    name = get_slot(slots['Name'])
    city = get_slot(slots['City'])
    cuisine = get_slot(slots['Cuisine'])
    num_people = get_slot(slots['NPeople'])
    dining_date =  get_slot(slots['DinningDate'])  
    dining_time = get_slot(slots['DiningTime'])
    phone = get_slot(slots['Phone'])
    print("\nSlots:")
    print(slots)
    print('\nName:')
    print(name)
    
    #get invocation source
    invocation_source = intent_request['invocationSource']
    
    cities_info = ['new york']
    cousines_info = ['japanese', 'chinese', 'korean', 'american', 'caribbean', 'bbq', 'burgers', 'pizza', 'mexican']
    
    #handle
    if invocation_source == 'DialogCodeHook':
        #check violation and if it is send appropiate response
        if city is not None and city.lower() not in cities_info:
            slots['City'] = None
            
            resp = {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'City'
                    },
                    'intent': {
                        'name': intent_name,
                        "slots": slots,
                    }
                },
                'messages': [{
                    'contentType': 'PlainText',
                    'content': 'Sorry I dont know restaurants in there. What other city would you like to dine in?'
                }]
            }
           
            return resp
            
        elif cuisine is not None and cuisine.lower() not in cuisines_info:
            slots['Cuisine'] = None
            
            resp = {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'Cuisine'
                    },
                    'intent': {
                        'name': intent_name,
                        "slots": slots,
                    }
                },
                'messages': [{
                    'contentType': 'PlainText',
                    'content': 'Sorry I dont know that type of cuisine.  What othe type of cuisine would you like to try?'
                }]
            }
           
            return resp
            
        
        else:
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
        sqs = boto3.client('sqs')
        response = sqs.get_queue_url(QueueName='chatbot_queue')
        queue_url = response['QueueUrl']
        
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes={
                'name': {
                    'DataType': 'String',
                    'StringValue': name
                },
                'city': {
                    'DataType': 'String',
                    'StringValue': city
                },
                'cuisine': {
                    'DataType': 'String',
                    'StringValue': cuisine
                },
                'dining_date': {
                    'DataType': 'String',
                    'StringValue': dining_date
                },
                'dining_time': {
                    'DataType': 'String',
                    'StringValue': dining_time
                },
                'num_people': {
                    'DataType': 'String',
                    'StringValue': num_people
                },
                'phone': {
                    'DataType': 'String',
                    'StringValue': phone
                }
            },
            MessageBody=(
                'Results from chatbot conversation'
            )
        )
        
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
    elif intent_name == 'ThankYouIntent':
        return None
    else:
        #FallbackIntent
        return close_response(intent_request, intent_name)
        
        



def lambda_handler(event, context):
    # TODO implement
    return intent_handler(event)