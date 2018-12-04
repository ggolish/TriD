
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

    # Set username
    window = NameEntryWindow()
    username = window.get_name()
    client.set_username(username)

    # Choose an opponent
    window = OpponentChooseWindow(client.get_available_opponents)
    while True:
        opponent = window.choose_opponent()
        if client.initiate_game(username, opponent):
            break
    window.destroy()

    print(opponent)
    
#     game = TriD()
#     game.mainloop()
