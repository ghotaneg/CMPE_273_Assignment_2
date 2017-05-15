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


def post_order(event, context):
    # TODO implement
    order_table = boto3.resource('dynamodb').Table('Order')
    menu_table = boto3.resource('dynamodb').Table('Menu')

    # Get the details from Menu table for the menu_id passed in the order request.
    reply = menu_table.get_item(
        Key={"menu_id": event["menu_id"]},
        ProjectionExpression='menu_id,store_name,selection,size,price,store_hours')

    item = reply['Item']

    # Counter to display option numbers for selection.
    count = 1
    selection_items = ""

    # Looping over all the items in selection to add Option numbers like 1,2,3...etc.
    for s in item['selection']:
        if count == 1:
            selection_items = "1. " + str(s)
        else:
            selection_items += ", " + str(count) + ". " + str(s)
        count += 1

    # Insert a new row in 'Order' table.
    response = order_table.put_item(
        Item={'menu_id': event['menu_id'],
              'order_id': event['order_id'],
              'customer_name': event['customer_name'],
              'customer_email': event['customer_email'],
              'order_status': 'Pending'
              }
    )

    # Creating the final output to be displayed to the customer.
    output_msg = '{ "Message" : "Hi ' + event['customer_name'] + \
                 ', please choose one of these selection:  ' + selection_items + '"}'

    return json.dumps(output_msg, indent=4, cls=DecimalEncoder)




