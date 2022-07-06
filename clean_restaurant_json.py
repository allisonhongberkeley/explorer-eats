import json 
import re

#categories.json is a list of dictionaries 
file = open("categories.json")
obj = json.load(file)

for element in obj:
    if "restaurants" not in element["parents"]: 
        element.clear()
    if "country_whitelist" in element.keys():
        if "US" not in element["country_whitelist"]:
            element.clear()


remove_empty = json.dumps(obj)
remove_empty = re.sub('\{\},', '', remove_empty)
obj2 = json.loads(remove_empty)

open("restaurant-categories.json", "w").write(
    json.dumps(obj2, sort_keys=True, indent=4)
)