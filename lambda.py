import json
import boto3

def lambda_handler(event, context):
    # Set event to dish-name
    try:
        event = event['queryStringParameters']['dish-name']
    except:
        return { 'statusCode': 400, 'body': "'dish-name' not defined or defined incorrectly." }
        
    event = event.lower()
    
    # Read ingredients from S3
    try:
        item_ingredients = []
        s3_object = boto3.client('s3')
        s3_menu_object = s3_object.get_object(Bucket ='dominos-menu' , Key = 'menu.json')
        s3_item_data = s3_menu_object['Body'].read().decode('utf-8')
        s3_ingredients_list = json.loads(s3_item_data)
        # Get ingredients of dish
        dish_ingredients = s3_ingredients_list[event]
    except Exception:
        return { 'statusCode': 500, 'body': 'Failed to load s3 data'}

    try:
        # Load database and table
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('ingredients')
    except Exception:
        return { 'statusCode': 500, 'body': 'Failed to load dynamodb data' }
    
    try:
        # Create empty output
        newJson = {}
        for ingredient in dish_ingredients:
            # Fetch the ingredient values from the database
            ingr_vals = table.get_item(Key={'name': ingredient})['Item']
            # Create a new entry
            newJson[ingredient] = ingr_vals
            # Sanitize
            newJson[ingredient].pop('name')
    except Exception:
        return { 'statusCode': 500, 'body': 'Failed to populate newJson', 'newJson': newJson}
    
    vegan = True
    vegetarian = True
    gluten_free = True
    dairy_free = True
    peanut = False
    shellfish = False
    soy = False
    treenut = False
    allergen_free = True
    
    try:
        for ingredient in newJson:
            if(newJson[ingredient]['dairy_free'] != 'true'):
                dairy_free = False
            if(newJson[ingredient]['gluten_free'] != 'true'):
                gluten_free = False
            if(newJson[ingredient]['peanut'] == 'true'):
                allergen_free = False
                peanut = True
            if(newJson[ingredient]['shellfish'] == 'true'):
                allergen_free = False
                shellfish = True
            if(newJson[ingredient]['soy'] == 'true'):
                allergen_free = False
                soy = True
            if(newJson[ingredient]['treenut'] == 'true'):
                allergen_free = False
                treenut = True
            if(newJson[ingredient]['vegan'] != 'true'):
                vegan = False
            if(newJson[ingredient]['vegetarian'] != 'true'):
                vegetarian = False

    except Exception as e:
        return { 'statusCode': 500, 'message': 'Failed to apply booleans' }
    
    print("Reached the end. Returning...")
    response = {
        'statusCode': 200,
        'headers': {'Content-Type': 'aplication/json', 'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'},
        'body' : json.dumps({
            'ingredients': newJson,
            'allergen_free': allergen_free,
            'dairy_free': dairy_free,
            'gluten_free': gluten_free,
            'peanut': peanut,
            'shellfish': shellfish,
            'soy': soy,
            'treenut': treenut,
            'vegan': vegan,
            'vegetarian': vegetarian
        })
    }
    print("response: " + json.dumps(response))
    return response