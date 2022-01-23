import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ingredients')

file = open('ingredients.csv')

for line in file:
  contents = line.lower().split(",")
  ingredient = {}
  ingredient['name'] = contents[0].strip()
  ingredient['dairy_free'] = contents[1].strip()
  ingredient['gluten_free'] = contents[2].strip()
  ingredient['peanut'] = contents[3].strip()
  ingredient['shellfish'] = contents[4].strip()
  ingredient['soy'] = contents[5].strip()
  ingredient['treenut'] = contents[6].strip()
  ingredient['vegan'] = contents[7].strip()
  ingredient['vegetarian'] = contents[8].strip()
  with table.batch_writer() as batch:
    batch.put_item(Item=ingredient)