file = open('menu.csv', 'r')
save = open('menu.json', 'w')

output = {}
for line in file:
    contents = line.lower().split(',')
    name = contents.pop(0)
    
    ingredients = {}
    for ingredient in contents:
        ingredients[ingredient.strip("\n")] = ""
    
    output[name] = ingredients

print(output)