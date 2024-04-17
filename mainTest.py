import json
import boto3

lambda_client = boto3.client('lambda')
sts_client = boto3.client('sts')

def get_account_id():
    response = sts_client.get_caller_identity()
    return response['Account']

def invoke_lambda_function(function_name, payload):

    account_id = get_account_id()

    arn = f"arn:aws:lambda:eu-central-1:{account_id}:function:{function_name}"

    response = lambda_client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    return json.load(response["Payload"])

def main_test(event, context):
    # Write Multiple Items
    write_items_params = {
        "items": [
            {"Name": "Mammadli", "Vorname": "Tural", "Mail": "tmammadli@gmx.de", "Geburtstag": "27-09-1998", "PLZ": "91746", "Geschlecht": "Mann", "secret": "tm123", "Systemrelevanz" : 1, "Vorerkrankungen": 1},
            {"Name": "Mammadli", "Vorname": "Huseyn", "Mail": "hmammadli@gmx.de", "Geburtstag": "10-09-1996", "PLZ": "96052", "Geschlecht": "Mann", "secret": "hm123","Systemrelevanz" : 1, "Vorerkrankungen": 1}
        ]
    }



    {
  "ID": 20240118002510111408,
  "Name": "Aliyev"
}
    
    {
  "PLZ": 20240118133238249499
}
    write_response = invoke_lambda_function("Aufgabe2-dev-writeItem", write_items_params)

    print("Response of writeItems:")
    print(write_response)
    print("\n")

