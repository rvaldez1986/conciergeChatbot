import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print('\nEvent: ')
    print(event)
    print('\nContext: ')
    print(context)
    
    
    # LexV2 client uses 'lexv2-runtime'
    client = boto3.client('lexv2-runtime', region_name='us-east-1')

    response = client.recognize_text(
        botId='NQ5ASUGSBJ',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId="test_session",
        text=event['messages'][0]['unstructured']['text'])  
        
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response["messages"][0]['content'])
    }