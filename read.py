import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ingredients')

resp = table.get_item(Key={"name": "beef"})

print(resp['Item'])