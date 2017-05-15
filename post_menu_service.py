# -*- coding: utf-8 -*-
import boto3


def post_menu(event, context):
    # Your code goes here!

    dynamodb = boto3.resource('dynamodb').Table('Menu')

    response = dynamodb.put_item(
        Item={'menu_id': event['menu_id'],
              'store_name': event['store_name'],
              'selection': event['selection'],
              'size': event['size'],
              'price': event['price'],
              'store_hours': event['store_hours']
              }
    )

    return "200 OK"
