import json
import boto3

client = boto3.resource('dynamodb')

def deleteItem(event, context):
    table = client.Table('MyVaccinTable')

    if 'IDs' not in event or not isinstance(event['IDs'], list):
        return "Invalid input. 'IDs' key with a list of IDs is required."

    deleted_entries = []

    for item_id in event['IDs']:
        try:
            response = table.delete_item(Key={'ID': item_id})
            deleted_entries.append({'ID': item_id, 'Status': 'Entry successfully deleted'})
        except client.exceptions.ClientError as e:
            deleted_entries.append({'ID': item_id, 'Status': f'Error: {str(e)}'})

    return deleted_entries