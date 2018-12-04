
import pygame
from utils import load_sprite

class Piece():

    def __init__(self, white, image_path, width):
        self.white = white
        self.image = load_sprite(image_path)
        self.image = pygame.transform.scale(self.image, (width, width))

    def draw(self, window, x, y):
        window.blit(self.image, (x, y))

class Pawn(Piece):

    def __init__(self, white, width):
        if white:
            image_path = "assets/pawn_white.png"
        else:
            image_path = "assets/pawn_black.png"
        super().__init__(white, image_path, width)

class Rook(Piece):

    def __init__(self, white, width):
        if white:
            image_path = "assets/rook_white.png"
        else:
            image_path = "assets/rook_black.png"
        super().__init__(white, image_path, width)

class Knight(Piece):

    def __init__(self, white, width):
        if white:
            image_path = "assets/knight_white.png"
        else:
            image_path = "assets/knight_black.png"
        super().__init__(white, image_path, width)

class Bishop(Piece):

    def __init__(self, white, width):
        if white:
            image_path = "assets/bishop_white.png"
        else:
            image_path = "assets/bishop_black.png"
        super().__init__(white, image_path, width)

class King(Piece):

    def __init__(self, white, width):
        if white:
            image_path = "assets/king_white.png"
        else:
            image_path = "assets/king_black.png"
        super().__init__(white, image_path, width)

class Queen(Piece):

    def __init__(self, white, width):
        if white:
            image_path = "assets/queen_white.png"
        else:
            image_path = "assets/queen_black.png"
        super().__init__(white, image_path, width)


