
'''
    Functions used by server for interacting with clients
'''

import json

# Global variables for tracking connections
users = {}
sockets = []


# Stores a new user's socket
def add_user(socket):
    global sockets
    print("connection made:", socket)
    sockets.append(socket)


# Removes a user
def remove_user(socket):
    global sockets
    global users
    print("connection dropped:", socket)
    for username, user in users.items():
        if user["socket"] == socket:
            del users[username]
            break
    sockets.remove(socket)


# Handles all messages sent from clients
def process_message(socket, message):
    global users
    message = json.loads(message)
    if message["type"] == "connect":
        users[message["username"]] = {"socket": socket}
    elif message["type"] == "getavailable":
        send_all_available_users(message["username"])
    elif message["type"] == "choose":
        users[message["opponent"]]["request"] = message["username"]
        users[message["username"]]["opponent"] = message["opponent"]
    elif message["type"] == "reply":
        if message["accepted"] is True:
            users[message["username"]]["opponent"] = message["opponent"]
            users[message["opponent"]]["socket"].write_message(message)
        else:
            del users[message["opponent"]]["opponent"]
            users[message["opponent"]]["socket"].write_message(message)
    elif message["type"] == "move":
        users[message["opponent"]]["socket"].write_message(message)


# Sends a user all available opponents. If a request has been made, it
# sends the request instead
def send_all_available_users(username):
    global users

    # Check if a request has been made
    if "request" in users[username]:
        message = json.dumps(
            {"type": "request", "opponent": users[username]["request"]})
        users[username]["socket"].write_message(message)
        del users[username]["request"]
        return

    # Send everything
    usernames = []
    for u, user in users.items():
        if user["socket"] not users[username]["socket"] and "opponent" not in user:
            usernames.append(u)
    users[username]["socket"].write_message(
        json.dumps({"type": "all", "users": usernames}))
