
import pygame

class Board():

    def __init__(self, x, y, width, size):
        self.x = x
        self.y = y
        self.width = width
        self.size = size

    def draw(self, window):
        ycurr = self.y
        white = True
        for i in range(self.size):
            old = white
            xcurr = self.x
            for j in range(self.size):
                if white:
                    c = (255, 255, 255)
                else:
                    c = (25, 25, 25)
                pygame.draw.rect(window, c, (xcurr, ycurr, self.width, self.width))
                xcurr += self.width
                white = not white
            white = not old
            ycurr += self.width

    def outline(self, window, color):
        pygame.draw.rect(window, color, (self.x - 1, self.y - 1, self.width * self.size + 1, self.width * self.size + 1), 5)

class CaptureBoard(Board):

    def __init__(self, x, y, width):
        super().__init__(x, y, width, 2)

