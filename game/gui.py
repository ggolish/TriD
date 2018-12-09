
import pygame

class GUI():

    def __init__(self, grid_width, start_x, start_y, end_x, end_y, player1):
        # State and geometry variables
        self.grid_width = grid_width
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.player1 = player1

        # Move text entry 
        self.move_box_x = self.start_x 
        self.move_box_y = self.start_y + 1
        self.move_box_line_start = start = (self.move_box_x * self.grid_width, (self.move_box_y + 1) * self.grid_width)
        self.move_box_line_end = (self.end_x * self.grid_width, (self.move_box_y + 1) * self.grid_width)


    def update(self):
        pass

    def draw(self, window):
        pygame.draw.line(window, (255, 255, 255), self.move_box_line_start, self.move_box_line_end)
