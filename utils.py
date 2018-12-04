
import pygame

sprites = {}

def load_sprite(path):
    global sprites

    if path not in sprites:
        sprites[path] = pygame.image.load(path)
    return sprites[path]
