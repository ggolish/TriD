
users = {}

def add_user(socket):
    global users
    users[socket] = {}

def remove_user(socket):
    global users
    del users[socket]

def process_message(socket, message):
    print(message)
