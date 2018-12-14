
import pygame

sprites = {}


# Loads a sprite into the global sprite table and returns it
def load_sprite(path):
    global sprites

    if path not in sprites:
        sprites[path] = pygame.image.load(path)
    return sprites[path]
