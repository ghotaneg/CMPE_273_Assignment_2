import boto3


def put_menu(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb').Table('Menu')
    key_value = event["menu_id"]

    for k, v in event.items():
        if k == "menu_id":
            pass
        else:
            upd_string = "set " + k + "=:a"
            response = dynamodb.update_item(
                Key={
                    "menu_id": key_value
                },
                UpdateExpression=upd_string,
                ExpressionAttributeValues={
                    ':a': v
                },
                ReturnValues="UPDATED_NEW"
            )

    return "200 OK"