import pygame

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = 10
        self.color = (255, 0, 0)

    def move(self):
        self.rect.x += self.speed

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
