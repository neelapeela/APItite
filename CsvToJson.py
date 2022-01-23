file = open("ingredients - Ingredients.csv", "r")
new = open("output.json", "w")

for line in file:
  contents = line.split(",")
  output  = '{'
  output += '"name": "' + contents[0].lower() + '",'
  output += '"dairy_free": ' + contents[2].lower() + ","
  output += '"gluten_free": ' + contents[7].lower() + ","
  output += '"peanut": ' + contents[1].lower() + ","
  output += '"shellfish": ' + contents[3].lower() + ","
  output += '"soy": ' + contents[8].lower().strip() + ","
  output += '"treenut": ' + contents[5].lower() + ","
  output += '"vegan": ' + contents[6].lower() + ","
  output += '"vegetarian": ' + contents[4].lower() + ""
  output += '}\n'
  new.write(output)
