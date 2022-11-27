import os
import json
from string import Template
import base64
import re
import shutil


def pass_encode(password):
    enpass = password.encode()
    encoded = base64.b64encode(enpass)
    return encoded


def pass_decode(encoded):
    dencode = base64.b64decode(encoded)
    decoded = dencode.decode()
    return decoded


def set_json(path, set_data, key):
    with open(path, 'r+') as f:
        data = json.load(f)
        data[key].append(set_data)
        f.seek(0)
        json.dump(data, f, indent=4)


def get_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data

def reminder_template(type, message):
    udata_template = Template("""{
            \"type\": \"$type\",
            \"message\": \"$message\"
            }""")
    dataforinsertion = udata_template.substitute(type=type, message=message)
    data_set = json.loads(dataforinsertion)
    return data_set

def new_user_template(name, password):
    udata_template = Template("""{
            \"name\": \"$name\",
            \"pass\": \"$password\"
            }""")
    dataforinsertion = udata_template.substitute(name=name, password=password)
    in_json_format = json.loads(dataforinsertion)
    return in_json_format


def get_reminders(username):
    path = f"./reminders/{username}/{username}.json"
    data = get_json(path)
    print("below are your reminders")
    print(data['reminders'][1:len(data['reminders'])])

