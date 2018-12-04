
import websocket
import json
import socket

class Client():

    def __init__(self):
        self.ws = websocket.WebSocket(sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),))

    def connect(self, address):
        self.ws.connect(address)

    def set_username(self, username):
        message = json.dumps({"type": "connect", "username": username})
        self.ws.send(message)

    def get_available_opponents(self):
        message = json.dumps({"type": "getavailable"})
        return json.loads(self.ws.recv())

    def initiate_game(self, username, opponent):
        return True