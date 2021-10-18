# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 00:52:42 2021

@author: rober
"""
import boto3
import json
from decimal import Decimal
from datetime import datetime

DATA = 'korean'

def get_elem(m_object, elem):
    if elem in m_object:
        return m_object[elem]
    else:
        return None
    


def lambda_handler(event, context):
    
    dynamodbclient=boto3.resource('dynamodb')
    sample_table = dynamodbclient.Table('yelp-restaurants')

    with open('{}_data.json'.format(DATA), 'r') as myfile:
        data=myfile.read()

    # parse file
    objects = json.loads(data, parse_float=Decimal)
    
    
    for m_object in objects['businesses']:
        id = m_object["id"]
        location = get_elem(m_object, "location")
        address = get_elem(location, "address1")
        z_code = get_elem(location, "zip_code")
        reviews = get_elem(m_object, "review_count")
        rating = get_elem(m_object, "rating")
        address = get_elem(location, "address1")
        z_code = get_elem(location, "zip_code")
        
        try:
            response=sample_table.put_item(
                Item={
                    'id': id,
                    'cuisine': DATA,
                    'address': address,
                    'zip_code': z_code,
                    'review_count': reviews,
                    'rating': rating,
                    'insertedAtTimestamp': str(datetime.now())
                    },
                    ConditionExpression='attribute_not_exists(id)'
                            
                )
        except:
            #item id was already there
            pass
    
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda LF2!')
    }