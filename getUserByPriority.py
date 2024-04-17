import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyVaccinTable')


def get_user_by_priority(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MyVaccinTable')

    prio = event.get("prio")

    try:
        response = table.query(
            TableName='MyVaccinTable',
            IndexName='PriorityIndex',
            Select='ALL_PROJECTED_ATTRIBUTES',
            KeyConditionExpression=Key('Priorisierungsgruppe').eq(prio)
        )
        return response.get("Items", [])
    except Exception as e:
        print(f"An error occurred: {e}")
        return []