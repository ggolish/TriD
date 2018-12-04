
import json

users = {}

def add_user(socket):
    global users
    print("connection made:", socket)
    users[socket] = {}

def remove_user(socket):
    global users
    print("connection dropped:", socket)
    del users[socket]

def process_message(socket, message):
    global users
    message = json.loads(message)
    if message["type"] == "connect":
        users[socket]["username"] = message["username"]
    elif message["type"] == "getavailable":
        send_all_available_users(socket)

def send_all_available_users(socket):
    global users
    usernames = []
    print(users)
    for s, u in users.items():
        if s != socket and "username" in u and "opponent" not in u:
            usernames.append(u["username"])
    socket.write_message(json.dumps(usernames))
