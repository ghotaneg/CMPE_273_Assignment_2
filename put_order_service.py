import boto3
import json
import decimal
import datetime
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


def put_order(event, context):
    # TODO implement
    order_table = boto3.resource('dynamodb').Table('Order')
    menu_table = boto3.resource('dynamodb').Table('Menu')

    # Get the details from Menu table for the menu_id passed in the order request.
    order_data = order_table.get_item(
        Key={'order_id': event['order_id']},
        ProjectionExpression='menu_id,order_id,customer_name,customer_email,order_status,#O',
        ExpressionAttributeNames = {
            '#O': 'order'
        }
    )
    order_item = order_data['Item']

    # Get the details from Menu table for the menu_id passed in the order request.
    menu_data = menu_table.get_item(
        Key={"menu_id": order_item['menu_id']},
        ProjectionExpression='menu_id,store_name,selection,size,price,store_hours')

    menu_item = menu_data['Item']

    if order_item['order_status'] == 'Pending':
        # Update the 'selection' field in the order table for the current order.
        upd_sel_response = order_table.put_item(
            Item={'menu_id': order_item['menu_id'],
                  'order_id': order_item['order_id'],
                  'customer_name': order_item['customer_name'],
                  'customer_email': order_item['customer_email'],
                  'order_status': 'Incomplete',
                  'order': {
                      "selection": menu_item['selection'][int(event['input'])-1],
                      "size": '0',
                      "costs": '0',
                      "order_time": datetime.datetime.now().strftime("%m-%d-%Y@%H:%M:%S")
                  }
                  }
        )

        # Counter to display option numbers for selection.
        count = 1
        size_items = ""

        # Looping over all the items in selection to add Option numbers like 1,2,3...etc.
        for s in menu_item['size']:
            if count == 1:
                size_items = "1. " + str(s)
            else:
                size_items += ", " + str(count) + ". " + str(s)
            count += 1

        # Creating the final output to be displayed to the customer.
        selection_output_msg = '{ "Message": "Which size do you want? ' + size_items + '"}'

        return json.dumps(selection_output_msg, indent=4, cls=DecimalEncoder)

    elif order_item['order_status'] == 'Incomplete':

        # Update the order with all the final details and costs.

        upd_order_response = order_table.put_item(
            Item={'menu_id': order_item['menu_id'],
                  'order_id': order_item['order_id'],
                  'customer_name': order_item['customer_name'],
                  'customer_email': order_item['customer_email'],
                  'order_status': 'processing',
                  'order': {
                      "selection": order_item['order']['selection'],
                      "size": menu_item['size'][int(event['input'])-1],
                      "costs": menu_item['price'][int(event['input'])-1],
                      "order_time": datetime.datetime.now().strftime("%m-%d-%Y@%H:%M:%S")
                  }
                  }
        )

        # Creating the final output to be displayed to the customer.
        output_msg = '{ "Message": "Your order costs ' + menu_item['price'][int(event['input'])-1] \
                     + '. We will email you when the order is ready. Thank you!"}'

        return json.dumps(output_msg, indent=4, cls=DecimalEncoder)

    else:
        return "No incomplete orders. Please place a new order first!"



