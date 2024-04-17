import boto3
from boto3.dynamodb.conditions import Key, Attr

def get_user_by_zipcode(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MyVaccinTable')

    plz = event.get("PLZ")

    try:
        response = table.query(
            TableName='MyVaccinTable',
            IndexName='PLZIndex',
            Select='ALL_PROJECTED_ATTRIBUTES',
            KeyConditionExpression=Key('PLZ').eq(plz) & Key('Priorisierungsgruppe').lte(3)
        )
        return response.get("Items", [])
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
