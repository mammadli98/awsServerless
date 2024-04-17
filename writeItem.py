import json
import boto3
from datetime import datetime, date
import re

client = boto3.resource('dynamodb')
table = client.Table('MyVaccinTable')

def validate_email(email):
    # Simple email validation using regular expression
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def validate_name(name):
    # Check if the name contains only alphabets
    return name.isalpha()

def validate_gender(gender):
    # Check if the gender is either 'Mann' or 'Frau'
    return gender.lower() in ['mann', 'frau']

def validate_plz(plz):
    # Check if PLZ consists of exactly 5 numeric digits
    return plz.isdigit() and len(plz) == 5

def validate_item(item):
    if not validate_name(item["Name"]) or not validate_name(item["Vorname"]):
        return f"Invalid name format for item {item}"

    if not validate_email(item["Mail"]):
        return f"Invalid email format for item {item}"

    if not validate_gender(item["Geschlecht"]):
        return f"Invalid gender for item {item}. Allowed values are 'Mann' or 'Frau'."
    
    if not validate_plz(item["PLZ"]):
        return f"Invalid PLZ format for item {item}. PLZ should be a 5-digit number."


    return None  # Validation passed

def calculate_priority(age, sysRel, vorerkrankung):
    prio = 0
    if age >= 60:
        prio = 1
    elif age < 60 and age >= 40:
        prio = 2
    elif age < 18:
        prio = -1
    else:
        prio = 3

    if prio == 3 and (sysRel or vorerkrankung):
        prio = 2
    
    return prio

def add_item_to_table(item):
    try:
        table.put_item(Item=item)
        return "Entry added!"
    except Exception as e:
        return f"Error adding entry: {str(e)}"

def write_items(items):
    responses = []
    for item in items:
        validation_result = validate_item(item)
        if validation_result:
            responses.append(validation_result)
            continue

        birth_date = datetime.strptime(item['Geburtstag'], "%d-%m-%Y").date()
        today = datetime.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        sysRel = item["Systemrelevanz"]
        vorerkrankung = item["Vorerkrankungen"]


        birth_day_month = item['Geburtstag'][0:5]
        item['GeburtsTagMonat'] = birth_day_month
        item['Priorisierungsgruppe'] = calculate_priority(age, sysRel, vorerkrankung)
        item['ID'] = int(datetime.now().strftime("%Y%m%d%H%M%S%f"))

        response = add_item_to_table(item)
        responses.append(response)
    
    return responses

def writeItem(event, context):
    if 'items' in event and isinstance(event['items'], list):
        return write_items(event['items'])
    else:
        return "Invalid input. 'items' key with a list of items is required."