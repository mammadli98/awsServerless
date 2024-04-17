import json
import boto3

client = boto3.resource('dynamodb')

def readItem(event, context):
    table = client.Table('MyVaccinTable')

    if 'IDs' not in event or not isinstance(event['IDs'], list):
        return "Invalid input. 'IDs' key with a list of IDs is required."

    retrieved_entries = []

    for item_id in event['IDs']:
        ret_table = table.get_item(Key={'ID': item_id})
        try:
            retrieved_entries.append(ret_table["Item"])
        except KeyError as e:
            retrieved_entries.append(f'No entry with ID {item_id} found!')

    return retrieved_entries