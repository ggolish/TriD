
'''
    Adds users to the server for debugging purposes
'''

from client import Client

if __name__ == "__main__":

    usernames = ["harry", "sally", "bob", "jerry", "marge"]
    clients = []
    for i in range(len(usernames)):
        clients.append(Client())
        clients[-1].connect("ws://localhost:8080")
        clients[-1].set_username(usernames[i])

    while True:
        continue
