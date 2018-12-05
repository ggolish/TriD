
import json

users = {}
sockets = []

def add_user(socket):
    global sockets
    print("connection made:", socket)
    sockets.append(socket)

def remove_user(socket):
    global sockets
    global users
    print("connection dropped:", socket)
    for username, user in users.items():
        if user["socket"] == socket:
            del users[username]
            break
    sockets.remove(socket)

def process_message(socket, message):
    global users
    message = json.loads(message)
    if message["type"] == "connect":
        users[message["username"]] = {"socket": socket}
    elif message["type"] == "getavailable":
        send_all_available_users(message["username"])
    elif message["type"] == "choose":
        users[message["opponent"]]["request"] = message["username"]

def send_all_available_users(username):
    global users

    # Check if a request has been made
    if "request" in users[username]:
        message = json.dumps({"type": "request", "opponent": users[username]["request"]})
        users[username]["socket"].write_message(message)
        return

    # Send everything
    usernames = []
    for u, user in users.items():
        if user["socket"] != users[username]["socket"] and "opponent" not in user:
            usernames.append(u)
    users[username]["socket"].write_message(json.dumps({"type": "all", "users": usernames}))

