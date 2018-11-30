
import pygame

from board import Board, CaptureBoard

# Dictionary describing the different states the game can be in at any 
# given time
game_status = {
    "INIT": 0,      # The game has been initialized, but the mainloop has not been called
    "NORMAL": 1,    # The game is in the mainloop and running normally
    "FINISHED": 2   # The game is over and the mainloop should be broken
}

class TriD():

    def __init__(self, debug=False):

        # Initialize pygame variables
        pygame.init()
        if debug:
            self.width = 800
            self.height = 600
            self.main_window = pygame.display.set_mode((self.width, self.height))
        else:
            self.main_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.main_window.get_size()

        # Initialize state variables
        self.status = game_status["INIT"]
        self.debug = debug

        # Calculate geometry of play area
        self.grid_space = min(self.width, self.height) // 12
        self.grid_width = self.width // self.grid_space
        self.grid_height = self.height // self.grid_space
        self.board_start_x = (self.grid_width - 6) // 2
        self.board_start_y = (self.grid_height - 10) // 2
        self.board_end_x = self.grid_width - self.board_start_x - 1
        self.board_end_y = self.grid_height - self.board_start_y - 1

        # Initialize boards
        self.main1 = Board((self.board_start_x + 1) * self.grid_space, (self.board_start_y + 1) * self.grid_space, self.grid_space, 4)
        self.main2 = Board((self.board_start_x + 1) * self.grid_space, (self.board_start_y + 3) * self.grid_space, self.grid_space, 4)
        self.main3 = Board((self.board_start_x + 1) * self.grid_space, (self.board_start_y + 5) * self.grid_space, self.grid_space, 4)
        self.cb1 = CaptureBoard((self.board_start_x) * self.grid_space, (self.board_start_y) * self.grid_space, self.grid_space)
        self.cb2 = CaptureBoard((self.board_start_x + 4) * self.grid_space, (self.board_start_y) * self.grid_space, self.grid_space)
        self.cb3 = CaptureBoard((self.board_start_x) * self.grid_space, (self.board_start_y + 8) * self.grid_space, self.grid_space)
        self.cb4 = CaptureBoard((self.board_start_x + 4) * self.grid_space, (self.board_start_y + 8) * self.grid_space, self.grid_space)

        # Zlevels
        self.zlevel = [None] * 7
        self.zlevel[6] = [self.cb1, self.cb2]
        self.zlevel[5] = [self.main1]
        self.zlevel[3] = [self.main2]
        self.zlevel[2] = [self.cb3, self.cb4]
        self.zlevel[1] = [self.main3]

        # Colors for each zlevel
        self.zcolor = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255),
            (128, 128, 128)
        ]

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.status = game_status["FINISHED"]

    def update(self):
        pass

    def draw(self):
        self.main_window.fill((0, 0, 0))

        if self.debug:
            self.draw_grid()

        for z in range(len(self.zlevel)):
            li = self.zlevel[z]
            if li:
                for b in li:
                    b.draw(self.main_window)
                    b.outline(self.main_window, self.zcolor[z])

        pygame.display.flip()

    def draw_grid(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if x >= self.board_start_x and y >= self.board_start_y and x <= self.board_end_x and y <= self.board_end_y:
                    c = (0, 255, 0)
                else:
                    c = (25, 25, 25)
                pygame.draw.rect(self.main_window, c, (x * self.grid_space, y * self.grid_space, self.grid_space, self.grid_space), 1)


