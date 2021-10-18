import json
import boto3
import urllib3
from base64 import b64encode
from boto3.dynamodb.conditions import Key, Attr



def lambda_handler(event, context):
    # TODO implement
    print("This is LF2")
    
    #Params for SQS
    sqs = boto3.client('sqs')
    response = sqs.get_queue_url(QueueName='chatbot_queue')
    queue_url = response['QueueUrl']
    print(queue_url)
    message = None
    
    #Params for openSearch
    userAndPass = b64encode(b"admin:Vamosroberto100%").decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass }
    http = urllib3.PoolManager()
    cuisine = None
    
    #Params for Dynamo
    dynamodbclient=boto3.resource('dynamodb')
    table = dynamodbclient.Table('yelp-restaurants')
    
    #Params for SNS
    sns = boto3.client('sns')
    
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    try:
    
        #Get message from SQS
        
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % message)
        
        #Parse the message
        person_name = message['MessageAttributes']['name']['StringValue']
        city = message['MessageAttributes']['city']['StringValue']
        cuisine = message['MessageAttributes']['cuisine']['StringValue']
        dining_date =  message['MessageAttributes']['dining_date']['StringValue']
        dining_time = message['MessageAttributes']['dining_time']['StringValue']
        num_people = message['MessageAttributes']['num_people']['StringValue']
        phone =  message['MessageAttributes']['phone']['StringValue']
        
        
        #Based on cuisine ask for a restaurant from OpenSearch
        
        r = http.request('GET', 'https://search-restaurants-kwrk7qrud3rbmlsdwr7mcqsj2m.us-east-1.es.amazonaws.com/restaurants/_search?q='+str(cuisine), headers=headers)
        data = json.loads(r.data)
        #Get restaurant ID from result
        RestaurantID = data['hits']['hits'][0]['_source']['id']
        print('restaurant id is')
        print(RestaurantID)
        
        #Query DynamoDB table with restaurant ID
        
        response2 = table.query(
                KeyConditionExpression=Key('id').eq(RestaurantID)
            )
        restaurant_name = response2['Items'][0]['name']
        address = response2['Items'][0]['address']
        num_reviews = response2['Items'][0]['review_count']
        rating = response2['Items'][0]['rating']
        zip_code = response2['Items'][0]['zip_code']
    
        #Create message
        
        sendMessage = "Hello {}! For {}, we recommend the {} {} restaurant on {}. The place has {} of reviews and an average score of {} on Yelp. Enjoy your Meal!".format(person_name, city, restaurant_name, cuisine, address, num_reviews, rating)
        
        # send message
        sns.publish(
            PhoneNumber = '+1'+phone,
            Message = sendMessage
        )

      
        
    except:
        print("SQS queue is now empty")
        
        
         
    # return 
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda LF2!')
    }