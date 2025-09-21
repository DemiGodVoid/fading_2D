import pygame

class Ground:
    def __init__(self, height):
        self.height = height
        self.color = (0, 200, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, win):
        self.rect = pygame.Rect(0, win.get_height() - self.height, win.get_width(), self.height)
        pygame.draw.rect(win, self.color, self.rect)
