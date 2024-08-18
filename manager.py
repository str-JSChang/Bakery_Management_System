import json
import os

# Open the JSON File
def load_users():
    # Without os.path.join, it would not join the current script path together with users.json
    file_path = os.path.join(os.path.dirname(__file__), 'users.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found. Returning an empty dictionary.")
        return {}

users = load_users()
print(users)

# Explaination of special variable __file__ is a special/method/variable to return the current path
#print(__file__)