from helper_functions import *
import os
import json
import re
import shutil


def add_new_user(name, password):
    encodedpass = pass_encode(password)
    result = new_user_template(name, encodedpass)
    key = 'user_details'
    path = "./user_details.json"
    set_json(path, result, key)


def register_new_user(username, password):
    path = "./user_details.json"
    if os.path.exists(path):
        data = get_json(path)
        all_users = data['user_details']
        users = []
        for i in range(len(all_users)):
            print(all_users[i]['name'])
            users.append(all_users[i]['name'])
        if username in users:
            print('username already present! choose a different name')
        else:
            print('adding user')
            add_new_user(username, password)
            print('successfully added new user')


def user_login(username, password, trials):
    print('validating user credentials')
    status = validate_credentials(username, password)
    if status:
        print('successfully logged in')
    elif trials == 0:
        print("tried more than 3 times exit!")
        exit()
    else:
        trials = trials - 1
        print('wrong user details provided try again')
        username = input("enter usrname\n")
        password = input("enter password \n")
        user_login(username, password, trials)


def validate_credentials(username, password):
    flag = False
    path = "./user_details.json"
    data = get_json(path)
    all_users = data['user_details']
    users = []
    for i in range(len(all_users)):
        users.append(all_users[i]['name'])
    if username in users:
        index = users.index(username)
        encodedpass = all_users[index]['pass']
        temp1 = re.sub(r"^b\'", "", encodedpass)
        temp2 = re.sub(r"\'$", "", temp1)
        value = bytes(temp2, 'utf8')
        decodedpass = pass_decode(value)
        if password == decodedpass:
            flag = True
    return flag




def set_reminder(type, message, username):
    print('setting new reminder')
    data_set = reminder_template(type, message)
    new_reminder(username, data_set)


def new_reminder(username, data_set):
    if os.path.exists(f'./reminders/{username}/{username}.json'):
        with open(f'./reminders/{username}/{username}.json', 'r+') as f:
            data = json.load(f)
            data['reminders'].append(data_set)
            f.seek(0)
            json.dump(data, f, indent=4)
            print('reminder set - if ')
    else:
        os.mkdir(f'./reminders/{username}')
        with open('./reminders/template.json') as f:
            temp_data = json.load(f)
        with open(f'./reminders/{username}/{username}.json', 'w') as f:
            json.dump(temp_data, f, indent=4)
            f.close()
        path = f'./reminders/{username}/{username}.json'
        with open(f'./reminders/{username}/{username}.json', 'r+') as f:
            data = json.load(f)
            data['reminders'].append(data_set)
            f.seek(0)
            json.dump(data, f, indent=4)
            print('reminder set - else')


def delete_user_details(name):
    path = "./user_details.json"
    data = get_json(path)
    user_details = data['user_details']
    users = []
    for i in range(len(user_details)):
        users.append(user_details[i]['name'])
    if name in users:
        index = users.index(name)
        print("are u sure you want to delete if yes")
        password = input('enter your password')
        encodedpass = user_details[index]['pass']
        temp1 = re.sub(r"^b\'", "", encodedpass)
        temp2 = re.sub(r"\'$", "", temp1)
        value = bytes(temp2, 'utf8')
        decodedpass = pass_decode(value)
        if password == decodedpass:
            data['user_details'].pop(index)
            print(data['user_details'])
            with open("./user_details.json", 'w') as f:
                f.seek(0)
                json.dump(data, f, indent=4)
            shutil.rmtree(f"./reminders/{name}")
    else:
        print("user details not found")

choice = True
print('welcome to reminder me app')
top_menu = ['1. New user registration',
            '2. User login',
            '3. Delete my details',
            '4. Logout']
reminder_menu = ['1. New reminder',
                 '2. View all reminders']
while choice:
    for i in range(len(top_menu)):
        print(top_menu[i])
    response = input('enter your choice\n')
    match response:
        case "1":
            print("registering new user")
            username = input("enter usrname\n")
            password = input("enter password \n")
            register_new_user(username, password)
        case "2":
            print("*** user login page ***")
            username = input("enter usrname\n")
            password = input("enter password \n")
            trials = 3
            user_login(username, password, trials)
            print(f'welcome {username} select from below choices')
            for i in range(len(reminder_menu)):
                print(reminder_menu[i])
            selector = input('enter your choice\n')
            match selector:
                case "1":
                    type = input('enter type of reminder:')
                    message = input("enter message:")
                    set_reminder(type, message, username)
                case "2":
                    try:
                        get_reminders(username)
                    except:
                        print("no reminders set ! if this is your first time set a reminder")
                        print(f'welcome {username} select from below choices')
                        for i in range(len(reminder_menu)):
                            print(reminder_menu[i])
                        selector = input('enter your choice\n')
                case _:
                    print("wrong choice")
        case "3":
            print('delete my user details')
            name = input("enter your username")
            delete_user_details(name)
        case "4":
            choice = False
            print('logging out')
        case _:
            print("wrong choice")





