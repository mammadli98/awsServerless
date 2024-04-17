import boto3
from boto3.dynamodb.conditions import Key

dynamodb_resource = boto3.resource('dynamodb')
dates_table = dynamodb_resource.Table('datesTable')
vacc_table = dynamodb_resource.Table('MyVaccinTable')
ses_client = boto3.client('ses')


def distribute_dates(event, context):
    try:
        plz_code = event.get("PLZ")
        number_of_dates = event.get("n")
        index = 0

        response_vacc = vacc_table.query(
            TableName='MyVaccinTable',
            IndexName='PLZIndex',
            Select='ALL_PROJECTED_ATTRIBUTES',
            KeyConditionExpression=Key('PLZ').eq(plz_code) & Key('Priorisierungsgruppe').lte(3),
            FilterExpression="attribute_not_exists(Termin)"
        )

        response_dates = vacc_table.query(
            TableName='datesTable',
            KeyConditionExpression=Key('PLZ').eq(plz_code)
        )

        entries = response_vacc.get("Items", [])
        dates = response_dates.get("Items", [])

        if number_of_dates is None:
            number_of_dates = len(entries)

        for date_entry in dates:
            date_count = len(date_entry.get("Termine", []))
            if date_count == number_of_dates:
                for time_entry in date_entry.get("Termine", []):
                    add_date_to_person(entries[index].get("ID"), entries[index].get("Mail"),
                                       date_entry.get("Datum"), time_entry)
                    index += 1

                dates_table.delete_item(
                    Key={'PLZ': plz_code, 'Datum': date_entry.get("Datum")}
                )
                break
            elif date_count > number_of_dates:
                date_copy = date_entry.get("Termine", [])
                for time_entry in date_entry.get("Termine", []):
                    add_date_to_person(entries[index].get("ID"), entries[index].get("Mail"),
                                       date_entry.get("Datum"), time_entry)
                    date_copy.remove(time_entry)
                    index += 1

                dates_table.update_item(
                    Key={'PLZ': plz_code, 'Datum': date_entry.get("Datum")},
                    UpdateExpression="SET Termine = :t",
                    ExpressionAttributeValues={':t': date_copy},
                    ReturnValues="UPDATED_NEW"
                )
                break
            else:
                for time_entry in date_entry.get("Termine", []):
                    add_date_to_person(entries[index].get("ID"), entries[index].get("Mail"),
                                       date_entry.get("Datum"), time_entry)
                    index += 1

                dates_table.delete_item(
                    Key={'PLZ': plz_code, 'Datum': date_entry.get("Datum")}
                )
                number_of_dates -= date_count

        return "Entry added!"

    except KeyError as e:
        return "Something went wrong ..."


def add_date_to_person(person_id, person_mail, appointment_date, appointment_time):
    vacc_table.update_item(
        Key={'ID': person_id},
        UpdateExpression="SET Termin = :t",
        ExpressionAttributeValues={':t': f"{appointment_date}-{appointment_time}"},
        ReturnValues="UPDATED_NEW"
    )

    ses_client.send_email(
        Source='tmammadli@gmx.de',
        Destination={'ToAddresses': [person_mail]},
        Message={
            'Subject': {'Data': 'Vaccination Appointment', 'Charset': 'utf-8'},
            'Body': {
                'Text': {'Data': f"Your vaccination appointment is on {appointment_date}, at {appointment_time}.",
                         'Charset': 'utf-8'}
            }
        }
    )