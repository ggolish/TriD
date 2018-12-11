
import pygame
import threading

from board import Board, CaptureBoard
from piece import *
from gui import *
from stars import Stars

# Dictionary describing the different states the game can be in at any 
# given time
game_status = {
    "INIT": 0,      # The game has been initialized, but the mainloop has not been called
    "NORMAL": 1,    # The game is in the mainloop and running normally
    "FINISHED": 2   # The game is over and the mainloop should be broken
}

class TriD():

    def __init__(self, client, debug=False):

        # Initialize pygame variables
        pygame.init()
        self.width = 1000
        self.height = 600
        self.main_window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TriD Chess ({}): Playing {}".format(client.username, client.opponent))
        self.clock = pygame.time.Clock()

        # Initialize state variables
        self.client = client
        self.player1 = True
        self.turn = self.client.get_player(self.player1)
        if self.turn == self.client.opponent:
            self.opponents_turn()
        self.status = game_status["INIT"]
        self.debug = debug

        # Calculate geometry of play area
        self.grid_space = min(self.width, self.height) // 12
        self.grid_width = self.width // self.grid_space
        self.grid_height = self.height // self.grid_space
        self.board_start_x = 1
        self.board_start_y = (self.grid_height - 10) // 2
        self.board_end_x = self.grid_width - self.board_start_x - 1
        self.board_end_y = self.grid_height - self.board_start_y - 1

        # Initialize GUI
        gui_init(int(self.grid_space * 0.9))
        self.move_command = ""
        self.upper = False
        self.background = Stars(800, self.width, self.height)

        # Initialize boards
        self.main1 = Board((self.board_start_x + 1) * self.grid_space, (self.board_start_y + 1) * self.grid_space, self.grid_space, 4)
        self.main2 = Board((self.board_start_x + 1) * self.grid_space, (self.board_start_y + 3) * self.grid_space, self.grid_space, 4)
        self.main3 = Board((self.board_start_x + 1) * self.grid_space, (self.board_start_y + 5) * self.grid_space, self.grid_space, 4)
        self.cb1 = CaptureBoard((self.board_start_x) * self.grid_space, (self.board_start_y) * self.grid_space, self.grid_space)
        self.cb2 = CaptureBoard((self.board_start_x + 4) * self.grid_space, (self.board_start_y) * self.grid_space, self.grid_space)
        self.cb3 = CaptureBoard((self.board_start_x) * self.grid_space, (self.board_start_y + 8) * self.grid_space, self.grid_space)
        self.cb4 = CaptureBoard((self.board_start_x + 4) * self.grid_space, (self.board_start_y + 8) * self.grid_space, self.grid_space)

        # Zlevels (which board pieces are on)
        self.zlevel = [None] * 7
        self.zlevel[6] = [self.cb1, self.cb2]
        self.zlevel[5] = [self.main1]
        self.zlevel[3] = [self.main2]
        self.zlevel[2] = [self.cb3, self.cb4]
        self.zlevel[1] = [self.main3]
        self.current_zlevel = 1

        # Rank / file system
        self.spaces = []
        for i in range(10):
            f = {}
            for j in range(6):
                f[chr(ord("a") + j)] = [None] * len(self.zlevel)
            self.spaces.append(f)

        # Initialize white pieces
        for i in range(1, 5):
            self.spaces[2][chr(ord('a') + i)][1] = Pawn(True, self.grid_space)
        self.spaces[1]['a'][2] = Pawn(True, self.grid_space)
        self.spaces[1]['b'][2] = Pawn(True, self.grid_space)
        self.spaces[0]['a'][2] = Rook(True, self.grid_space)
        self.spaces[0]['b'][2] = Queen(True, self.grid_space)
        self.spaces[1]['b'][1] = Knight(True, self.grid_space)
        self.spaces[1]['c'][1] = Bishop(True, self.grid_space)
        self.spaces[1]['d'][1] = Bishop(True, self.grid_space)
        self.spaces[1]['e'][1] = Knight(True, self.grid_space)
        self.spaces[0]['e'][2] = King(True, self.grid_space)
        self.spaces[0]['f'][2] = Rook(True, self.grid_space)
        self.spaces[1]['e'][2] = Pawn(True, self.grid_space)
        self.spaces[1]['f'][2] = Pawn(True, self.grid_space)

        # Initialize black pieces
        for i in range(1, 5):
            self.spaces[7][chr(ord('a') + i)][5] = Pawn(False, self.grid_space)
        self.spaces[8]['a'][6] = Pawn(False, self.grid_space)
        self.spaces[8]['b'][6] = Pawn(False, self.grid_space)
        self.spaces[9]['a'][6] = Rook(False, self.grid_space)
        self.spaces[9]['b'][6] = Queen(False, self.grid_space)
        self.spaces[8]['b'][5] = Knight(False, self.grid_space)
        self.spaces[8]['c'][5] = Bishop(False, self.grid_space)
        self.spaces[8]['d'][5] = Bishop(False, self.grid_space)
        self.spaces[8]['e'][5] = Knight(False, self.grid_space)
        self.spaces[9]['e'][6] = King(False, self.grid_space)
        self.spaces[9]['f'][6] = Rook(False, self.grid_space)
        self.spaces[8]['e'][6] = Pawn(False, self.grid_space)
        self.spaces[8]['f'][6] = Pawn(False, self.grid_space)

    def mainloop(self):
        self.status = game_status["NORMAL"]
        while self.status != game_status["FINISHED"]:
            self.process_input()
            self.update()
            self.draw()

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.status = game_status["FINISHED"]
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.change_zlevel(1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.change_zlevel(-1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                success = self.process_command(self.move_command)
                if success:
                    if self.turn == self.client.username:
                        self.client.send_move(self.move_command)
                        self.move_command = ""
                        self.player1 = not self.player1
                        self.turn = self.client.get_player(self.player1)
                        self.opponents_turn()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.move_command = self.move_command[:-1]
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                self.upper = True
            elif event.type == pygame.KEYUP and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                self.upper = False
            elif event.type == pygame.KEYDOWN:
                k = chr(event.key)
                if (k.isalnum() or k in " ,") and len(self.move_command) < 25:
                    if self.upper:
                        k = k.upper()
                    self.move_command += k

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.status = game_status["FINISHED"]

    def update(self):
        self.clock.tick(60)
        if self.turn == self.client.opponent:
            if self.client_thread.is_alive() == False:
                self.client_thread.join()
                self.player1 = not self.player1
                self.turn = self.client.get_player(self.player1)
        self.background.update()

    def draw(self):
        self.main_window.fill((0, 0, 0))

        self.background.draw(self.main_window)
        if self.debug:
            self.draw_grid()

        for z in range(len(self.zlevel)):
            if z == self.current_zlevel: continue
            li = self.zlevel[z]
            if li:
                for b in li:
                    b.draw(self.main_window)
                    self.draw_pieces(z)
                    b.outline(self.main_window, (0, 0, 0))

        if self.zlevel[self.current_zlevel]:
            for b in self.zlevel[self.current_zlevel]:
                b.draw(self.main_window)
                self.draw_pieces(self.current_zlevel)
                b.outline(self.main_window, (128, 0, 0))

        display_rank_file(0, 0, self.grid_space, self.main_window)
        display_turn(self.turn, 8, 0, self.grid_space, self.main_window)
        display_zlevel(self.current_zlevel + 1, 8, 1, self.grid_space, self.main_window)
        display_move(self.move_command, 8, 10, 11, self.grid_space, self.main_window)
        
        pygame.display.flip()

    def draw_grid(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                c = (25, 25, 25)
                pygame.draw.rect(self.main_window, c, (x * self.grid_space, y * self.grid_space, self.grid_space, self.grid_space), 1)

    def change_zlevel(self, offset):
        if offset != 1 and offset != -1:
            return
        self.current_zlevel += offset
        self.current_zlevel %= len(self.zlevel)
        li = self.zlevel[self.current_zlevel]
        while not li:
            self.current_zlevel += offset
            self.current_zlevel %= len(self.zlevel)
            li = self.zlevel[self.current_zlevel]

    def draw_pieces(self, z):
        for i in range(10):
            for j in range(6):
                r = i
                f = chr(ord('a') + j)
                p = self.spaces[r][f][z]
                if p != None:
                    x = (self.board_start_x + (ord(f) - ord('a'))) * self.grid_space
                    y = (self.board_start_y + (9 - r)) * self.grid_space
                    p.draw(self.main_window, x, y)
    
    def process_command(self, move):
        pieces = move.split("to")
        if len(pieces) != 2:
            print("Invalid command: case 1")
            return False

        src, dst = pieces

        sr, sf, sz = self.parse_position(src)
        dr, df, dz = self.parse_position(dst)

        if not sr or not dr:
            print("Invalid command: case 2")
            return False

        if self.spaces[sr][sf][sz] == None:
            print("Invalid command: case 3")
            return False

        self.spaces[dr][df][dz] = self.spaces[sr][sf][sz]
        self.spaces[sr][sf][sz] = None
        return True

    def parse_position(self, pos):
        pieces = pos.split(",")
        if len(pieces) != 3:
            return None, None, None

        # Parse rank
        try:
            r = int(pieces[0].strip()) 
        except:
            return None, None, None

        # Parse file
        f = pieces[1].strip()
        if not f.isalpha():
            return None, None, None

        # Parse zlevel
        try:
            z = int(pieces[2].strip()) - 1
        except:
            return None, None, None

        return r, f, z

    def opponents_turn(self):
        self.client_thread = threading.Thread(target=self.client.get_move, args=(self.process_command,))
        self.client_thread.daemon = True
        self.client_thread.start()

        
