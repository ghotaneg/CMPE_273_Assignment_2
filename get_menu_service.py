# -*- coding: utf-8 -*-
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def get_menu(event, context):
    # Your code goes here!

    dynamodb = boto3.resource('dynamodb').Table('Menu')


    response = dynamodb.get_item(
        Key={"menu_id": event["menu_id"]},
        ProjectionExpression='menu_id,store_name,selection,size,price,store_hours')

    item = response['Item']
    return json.dumps(item, indent=4, cls=DecimalEncoder)
