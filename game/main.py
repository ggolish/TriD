
import sys
from client import Client
from trid import TriD
from windows import NameEntryWindow, OpponentChooseWindow

def connect_to_server(address):
    return ws, username

if __name__ == "__main__":

    # Parse command line args
    if len(sys.argv) == 2:
        address = sys.argv[1]
    elif len(sys.argv) == 1:
        address = "ws://localhost:8080"
    else:
        sys.stderr.write("Usage: {} [server-address]\n".format(sys.argv[0]))
        sys.exit(1)

    # Connect to server
    client = Client()
    client.connect(address)

#     # Set username
#     window = NameEntryWindow()
#     username = window.get_name()
#     client.set_username(username)
# 
#     # Choose an opponent
#     while True:
#         window = OpponentChooseWindow(client.get_available_opponents)
#         opponent, t = window.choose_opponent()
#         window.destroy()
#         if not opponent or not t:
#             sys.exit(0)
#         if t == "request" and client.initiate_game(username, opponent):
#             break
#         elif t == "accept":
#             client.request_reply(opponent, True)
#             break
#         elif t == "deny":
#             client.request_reply(opponent, False)
# 
#     print("Playing against", opponent)
    
    game = TriD(client)
    game.mainloop()
