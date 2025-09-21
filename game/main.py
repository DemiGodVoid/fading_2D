import pygame
import random
import os
from ground import Ground
from zombie import Zombie, draw_tab, handle_tab_click
from player import Player
from bullets import Bullet

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)

ground_height = 100
ground = Ground(ground_height)

stand_img = pygame.image.load("game/stand.png")
walk_img = pygame.image.load("game/walk1.png")
player = Player(stand_img, walk_img, WIDTH//2, ground)

bullets = []
zombies = []
base_spawn_time = 60*60
current_spawn_time = base_spawn_time
zombie_timer = current_spawn_time
spawn_override_end_time = 0

if os.path.exists("game/points.txt"):
    with open("game/points.txt", "r") as f:
        try:
            points = int(f.read().strip())
        except:
            points = 0
else:
    points = 0

def save_points():
    with open("game/points.txt", "w") as f:
        f.write(str(points))

def handle_bullets():
    global points
    for b in bullets[:]:
        b.move()
        for z in zombies[:]:
            if b.rect.colliderect(z.rect):
                zombies.remove(z)
                if b in bullets:
                    bullets.remove(b)
                points += 5
                save_points()
                break
        if b.rect.x > WIN.get_width():
            if b in bullets:
                bullets.remove(b)
        else:
            b.draw(WIN)

def draw_score():
    score_text = font.render(f"Points: {points}", True, (255,255,255))
    WIN.blit(score_text, (WIN.get_width() - score_text.get_width() - 10, 10))

running = True
while running:
    dt = clock.tick(60)
    WIN.fill((50,50,50))

    ground.draw(WIN)
    player.ground = ground

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.draw(WIN)

    tab_rect = draw_tab(WIN)

    now_ticks = pygame.time.get_ticks()
    if spawn_override_end_time and now_ticks > spawn_override_end_time:
        current_spawn_time = base_spawn_time
        spawn_override_end_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                bullets.append(Bullet(player.rect.centerx, player.rect.top+25))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tab_rect.collidepoint(event.pos):
                if handle_tab_click(tab_rect):
                    points -= 20
                    save_points()
                    current_spawn_time = max(1, current_spawn_time // 2)
                    zombie_timer = current_spawn_time
                    spawn_override_end_time = now_ticks + 5*60*1000

    handle_bullets()

    zombie_timer -= 1
    if zombie_timer <= 0:
        zx = random.randint(ground.rect.left, ground.rect.right-40)
        zy = ground.rect.top-60
        zombies.append(Zombie(zx, zy))
        zombie_timer = current_spawn_time

    for z in zombies:
        z.move_towards(player.rect)
        z.draw(WIN)

    timer_seconds = zombie_timer // 60
    timer_text = font.render(f"Next zombie in: {timer_seconds}s", True, (255,255,0))
    WIN.blit(timer_text, (10,10))

    draw_score()
    pygame.display.update()

pygame.quit()
