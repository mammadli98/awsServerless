import boto3
from boto3.dynamodb.conditions import Key

def addition_new_dates(event, context):
    dynamodb = boto3.resource('dynamodb')
    dates_table = dynamodb.Table('datesTable')
    vacc_table = dynamodb.Table('MyVaccinTable')
    ses = boto3.client('ses')

    try:
        plz = event["PLZ"]
        datum = event["Datum"]
        termine = event["Termine"]
        i = 0

        response = vacc_table.query(
            TableName='MyVaccinTable',
            IndexName='PLZIndex',
            Select='ALL_PROJECTED_ATTRIBUTES',
            KeyConditionExpression=Key('PLZ').eq(plz) & Key('Priorisierungsgruppe').lte(3),
            FilterExpression="attribute_not_exists(Termin)")

        entries = response.get("Items", [])

        for entry in entries:
            for termin in termine:
                vacc_table.update_item(
                    Key={'ID': entry["ID"]},
                    UpdateExpression="SET Termin = :t",
                    ExpressionAttributeValues={':t': f"{datum}-{termin}"},
                    ReturnValues="UPDATED_NEW"
                )

                ses.send_email(
                    Source='tmammadli@gmx.de',
                    Destination={'ToAddresses': [entry["Mail"]]},
                    Message={
                        'Subject': {'Data': 'Impftermin', 'Charset': 'utf-8'},
                        'Body': {
                            'Text': {'Data': f"Your date is on {datum}, at {termin}.", 'Charset': 'utf-8'}
                        }
                    }
                )

                termine.remove(termin)

        existing_dates = dates_table.query(
            TableName='datesTable',
            KeyConditionExpression=Key('PLZ').eq(plz) & Key('Datum').eq(datum)
        ).get("Items", [])

        if existing_dates and termine:
            dates = existing_dates[0].get("Termine", []) + termine
            dates_table.update_item(
                Key={'PLZ': plz, 'Datum': datum},
                UpdateExpression="SET Termine = :t",
                ExpressionAttributeValues={':t': dates},
                ReturnValues="UPDATED_NEW"
            )

        return "Entry added!"

    except Exception as e:
        print(f"An error occurred: {e}")
        return []