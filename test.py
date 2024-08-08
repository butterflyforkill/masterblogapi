diction = {
    "1": {
        "username": "conor",
        "password": "1qweasd2"
    }
}

def fucnt():
    for user in diction.values():
        return user.get('username')
        
print(fucnt())