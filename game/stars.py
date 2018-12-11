
import pygame
import numpy
from random import randrange

class Stars():

    def __init__(self, count, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = min(max_x, max_y)
        self.origin = numpy.array([max_x / 2, max_y / 2])
        self.stars = []
        for i in range(count):
            self.stars.append(numpy.array([randrange(-max_x, max_x), randrange(-max_y, max_y), randrange(1, self.max_z)]))

    def update(self):
        for s in self.stars:
            s[2] -= 10
            if s[2] <= 0:
                s[0] = randrange(-self.max_x, self.max_x)
                s[1] = randrange(-self.max_y, self.max_y)
                s[2] = self.max_z

    def draw(self, window):
        for s in self.stars:
            npos = s[:2] / s[2] * self.max_z + self.origin
            pygame.draw.circle(window, (255, 255, 255), npos.astype("int32").tolist(), self.max_z // s[2])

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    stars = Stars(500, 800, 600)

    while True:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        stars.update()
        window.fill((0, 0, 0))
        stars.draw(window)
        pygame.display.flip()

