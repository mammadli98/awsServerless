import boto3
from boto3.dynamodb.conditions import Key
from datetime import date
import json
from decimal import Decimal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = boto3.resource('dynamodb')
clientl = boto3.client('lambda')
sts_client = boto3.client('sts')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def get_account_id():
    response = sts_client.get_caller_identity()
    return response['Account']

def checkDate(event, context):
    # Set current Date to today
    curDayMonth = date.today().strftime('%d-%m')

    # Query BirthDayMonth-GSI of vaccinationData to receive all PK_PersID with today as birth date
    table_name = 'MyVaccinTable'
    index_name = 'GeburtsTagMonatIndex'

    with client.Table(table_name).index(index_name) as index:
        try:
            response = index.query(
                KeyConditionExpression=Key('GeburtsTagMonat').eq(curDayMonth)
            )
        except Exception as e:
            logger.error(f"Error querying DynamoDB: {e}")
            return

    # Extract PK_PersID from the response
    pers_ids = [item['ID'] for item in response.get('Items', [])]

    # If list is not empty, call updatePerson for every ID in list
    if pers_ids:
        account_id = get_account_id()
        for pers_id in pers_ids:
            input_params = {"PersonID": str(pers_id)}
            try:
                response = clientl.invoke(
                    FunctionName=f"arn:aws:lambda:eu-central-1:{account_id}:function:Aufgabe2-dev-updatePrio",
                    InvocationType='RequestResponse',
                    Payload=json.dumps(input_params, cls=DecimalEncoder)
                )
            except Exception as e:
                logger.error(f"Error calling the function 'updatePrio': {e}")
