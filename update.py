import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import date

dynamodb = boto3.resource('dynamodb')
client = boto3.client('events')
table = dynamodb.Table('MyVaccinTable')
fnameUpdatePrio = 'Aufgabe3-dev-updatePrio'


def updateItem(event, context):
    try:
        response = table.update_item(
            Key={
                'ID': event["ID"]
            },
            UpdateExpression="SET Name= :n, Vorname= :v, Mail= :m, Geburtstag= :g, PLZ= :plz, Geschlecht= :ge, Priorisierungsgruppe= :p",
            ExpressionAttributeValues={
                ':n': event["Name"],
                ':v': event["Vorname"],
                ':m': event["Mail"],
                ':g': event["Geburtstag"],
                ':plz': event["PLZ"],
                ':ge': event["Geschlecht"],
                ':p': event["Priorisierungsgruppe"]
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def updatePrio(event, context):
    id = event["PersonID"]

    birthday = table.query( KeyConditionExpression=Key('ID').eq(id))

    splitDate = birthday["Items"][0]["Geburtstag"].split("-")
    birthDate = date(int(splitDate[2]), int(splitDate[1]), int(splitDate[0]))

    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))

    if age >= 60:
        prio = 1
    elif age < 60 and age >= 40:
        prio = 2
    else:
        prio = 3

    try:
        response = table.update_item(
            Key={
                'ID': id
            },
            UpdateExpression="set Priorisierungsgruppe = :p",
            ExpressionAttributeValues={
                ':p': prio
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def update_last_name(event, context):
    return update_item(event, 'Name')

def update_first_name(event, context):
    return update_item(event, 'Vorname')

def update_mail(event, context):
    return update_item(event, 'Mail')

def update_birthday(event, context):
    return update_item(event, 'Geburtstag')

def update_plz(event, context):
    return update_item(event, 'PLZ')

def update_gender(event, context):
    return update_item(event, 'Geschlecht')

def update_sys_rlv(event, context):
    return update_item(event, 'Systemrelevanz')

def update_helth_prio(event, context):
    return update_item(event, 'Vorerkrankungen')

def update_item(event, attribute):
    try:
        response = table.update_item(
            Key={'ID': event.get("ID")},
            UpdateExpression=f"SET #n = :val",
            ExpressionAttributeValues={':val': event.get(attribute)},
            ExpressionAttributeNames={"#n": attribute},
            ReturnValues="UPDATED_NEW"
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def update_old_data(event, context):
    plz = event["plz"]
    n = event["n"]

    response = table.query(
        TableName='MyVaccinTable',
        IndexName='PLZIndex',
        Select='ALL_PROJECTED_ATTRIBUTES',
        KeyConditionExpression=Key('PLZ').eq(plz) & Key('Priorisierungsgruppe').lte(3),
        FilterExpression="attribute_not_exists(Version)")

    entries = response.get("Items", [])[:n]

    try:
        for entry in entries:
            table.update_item(
                Key={'ID': entry['ID']},
                UpdateExpression="SET Systemrelevanz= :s, Vorerkrankungen= :vo, Version= :ve",
                ExpressionAttributeValues={':s': False, ':vo': False, ':ve': 1},
                ReturnValues="UPDATED_NEW"
            )

    except Exception as e:
        print(f"An error occurred: {e}")
        return []