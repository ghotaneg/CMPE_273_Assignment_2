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

def get_order(event, context):
    # Your code goes here!

    order_table = boto3.resource('dynamodb').Table('Order')


    response = order_table.get_item(
        Key={"order_id": event["order_id"]},
        ProjectionExpression='menu_id,order_id,customer_name,customer_email,order_status,#O',
        ExpressionAttributeNames={
        '#O': 'order'
    })

    item = response['Item']
    return json.dumps(item, indent=4, cls=DecimalEncoder)
