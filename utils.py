import json

def init_DB():
    with open("bytebash/data/users.json", "w") as users:
        users.write(json.dumps({}))
    with open("bytebash/data/recipes.json", "w") as recipes:
        recipes.write(json.dumps({}))
