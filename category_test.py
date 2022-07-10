import json

category_file = open("restaurant-categories.json")
categories = json.load(category_file)
category_dict = {}
for category in categories:
    title = category.get('title')
    alias = category.get('alias')
    category_dict[title] = alias

print(category_dict)