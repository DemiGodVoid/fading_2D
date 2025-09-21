import pygame
import sys
import subprocess
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voids Entertainment")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

title_font = pygame.font.SysFont("Arial", 72, bold=True)
button_font = pygame.font.SysFont("Arial", 40)

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

def fade_in_intro():
    text_surface = title_font.render("Voids Entertainment", True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    alpha_surface = pygame.Surface((WIDTH, HEIGHT))
    alpha_surface.fill(BLACK)
    for alpha in range(255, -1, -5):
        screen.fill(BLACK)
        screen.blit(text_surface, text_rect)
        alpha_surface.set_alpha(alpha)
        screen.blit(alpha_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)
    time.sleep(2)

def menu_screen():
    play_button = Button("Play", WIDTH//2 - 100, 250, 200, 60, lambda: run_script("game/main.py"))
    extract_button = Button("Extract Points", WIDTH//2 - 100, 350, 200, 60, lambda: run_script("game/extract.py"))
    buttons = [play_button, extract_button]
    while True:
        screen.fill(BLACK)
        title_surface = title_font.render("Fading", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button.check_click(event.pos)

def run_script(path):
    pygame.quit()
    subprocess.run(["python", path])
    sys.exit()

fade_in_intro()
menu_screen()

