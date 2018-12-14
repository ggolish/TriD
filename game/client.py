
'''
    Functions for interacting with the server
'''

import websocket
import json


class Client():

    def __init__(self):
        self.ws = websocket.WebSocket()
        self.username = None
        self.opponent = None
        self.player1 = None

    # Connects to the server
    def connect(self, address):
        self.ws.connect(address)

    # Sets the user's username on the server
    def set_username(self, username):
        message = json.dumps({"type": "connect", "username": username})
        self.username = username
        self.ws.send(message)

    # Asks the server for all available users
    def get_available_opponents(self):
        message = json.dumps(
            {"type": "getavailable", "username": self.username})
        self.ws.send(message)
        return json.loads(self.ws.recv())

    # Attempts to initiate a game between user and opponent
    def initiate_game(self, username, opponent):
        message = json.dumps(
            {"type": "choose", "username": username, "opponent": opponent})
        self.ws.send(message)
        response = json.loads(self.ws.recv())
        while response["type"] != "reply":
            response = self.ws.recv()
        if response["accepted"]:
            self.opponent = opponent
            self.player1 = True
        return response["accepted"]

    # Sends a reply to a game request
    def request_reply(self, opponent, accepted):
        if accepted:
            self.opponent = opponent
            self.player1 = False
        message = json.dumps({"type": "reply", "username": self.username,
                              "opponent": opponent, "accepted": accepted})
        self.ws.send(message)

    # Sends a move to the server
    def send_move(self, move):
        message = json.dumps({"type": "move", "username": self.username,
                              "opponent": self.opponent, "move": move})
        self.ws.send(message)

    # Gets a move from the server, meant to be run in it's own thread
    def get_move(self, callback):
        response = None
        while True:
            response = json.loads(self.ws.recv())
            if response["type"] == "move":
                break
        callback(response["move"])

    # Returns the username of the current player
    def get_player(self, player1):
        if player1:
            if self.player1:
                return self.username
            else:
                return self.opponent
        else:
            if self.player1:
                return self.opponent
            else:
                return self.username
