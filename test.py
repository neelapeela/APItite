import json
import boto3

# Load database and table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ingredients')
# Load input
data = json.load(open('input.json'))

# Create empty output
newJson = {}
for ingredient in event:
    # Fetch the ingredient values from the database
    ingr_vals = table.get_item(Key={'name': ingredient})['Item']
    # Create a new entry
    newJson[ingredient] = ingr_vals
    # Sanitize
    newJson[ingredient].pop('name')

print(newJson)