
import websocket
import json
import socket
import time

class Client():

    def __init__(self):
        self.ws = websocket.WebSocket()

    def connect(self, address):
        self.ws.connect(address)

    def set_username(self, username):
        message = json.dumps({"type": "connect", "username": username})
        self.username = username
        self.ws.send(message)

    def get_available_opponents(self):
        message = json.dumps({"type": "getavailable", "username": self.username})
        self.ws.send(message)
        return json.loads(self.ws.recv())

    def initiate_game(self, username, opponent):
        message = json.dumps({"type": "choose", "username": username, "opponent": opponent})
        self.ws.send(message)
        response = json.loads(self.ws.recv())
        while response["type"] != "reply":
            response = self.ws.recv()
        return response["accepted"]

    def request_reply(self, opponent, accepted):
        message = json.dumps({"type": "reply", "username": self.username, "opponent": opponent, "accepted": accepted})
        self.ws.send(message)
