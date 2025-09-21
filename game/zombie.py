import pygame
import os

class Zombie:
    def __init__(self, x, y, speed=1.0):
        self.speed = speed
        self.pos_x = float(x)
        self.stand_img = pygame.image.load(os.path.join("game", "zstand.png")).convert_alpha()
        self.walk_img = pygame.image.load(os.path.join("game", "zwalk1.png")).convert_alpha()
        self.stand_img = pygame.transform.scale(self.stand_img, (30, 45))
        self.walk_img = pygame.transform.scale(self.walk_img, (30, 45))
        self.image = self.stand_img
        self.walking = False
        self.animation_timer = 0
        self.animation_delay = 10
        self.rect = self.image.get_rect(topleft=(x, y))

    def move_towards(self, target_rect):
        self.walking = False
        if target_rect.x < self.rect.x:
            self.pos_x -= self.speed
            self.walking = True
        if target_rect.x > self.rect.x:
            self.pos_x += self.speed
            self.walking = True
        self.rect.x = int(self.pos_x)
        self.animation_timer += 1
        if self.walking and self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.image = self.walk_img if self.image == self.stand_img else self.stand_img
        elif not self.walking:
            self.image = self.stand_img

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

def draw_tab(win):
    width, height = 160, 60
    margin = 20
    x = win.get_width() - width - margin
    y = margin
    tab_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(win, (200, 50, 50), tab_rect, border_radius=5)
    font = pygame.font.Font(None, 24)
    text1 = font.render("Spawn SpeedX2", True, (255, 255, 255))
    text2 = font.render("20 points", True, (255, 255, 255))
    win.blit(text1, (x + 10, y + 10))
    win.blit(text2, (x + 10, y + 30))
    return tab_rect

def handle_tab_click(tab_rect):
    points_file = "game/points.txt"
    try:
        with open(points_file, "r") as f:
            points = int(f.read().strip())
    except:
        points = 0
    if points >= 20:
        points -= 20
        with open(points_file, "w") as f:
            f.write(str(points))
        return True
    return False
