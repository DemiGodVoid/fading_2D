import pygame
import sys
import requests

pygame.init()

WIDTH, HEIGHT = 700, 400
FONT = pygame.font.Font(None, 32)
SMALL_FONT = pygame.font.Font(None, 24)
BG_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extract Points")

button_rect = pygame.Rect(WIDTH//2 - 100, 50, 200, 50)
input_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 20, 300, 40)
enter_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 50, 120, 40)

input_active = False
input_text = ""
message = ""

API_URL = "https://vmpx.top/onelife/offline/update_points.php"
POINTS_FILE = "game/points.txt"

def draw():
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, GREEN, button_rect, border_radius=6)
    text = FONT.render("Extract Points", True, WHITE)
    screen.blit(text, (button_rect.centerx - text.get_width()//2,
                       button_rect.centery - text.get_height()//2))

    if input_active:
        pygame.draw.rect(screen, WHITE, input_rect, 2, border_radius=6)
        input_surface = FONT.render(input_text, True, WHITE)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.draw.rect(screen, GREEN, enter_rect, border_radius=6)
        enter_text = FONT.render("Enter", True, WHITE)
        screen.blit(enter_text, (enter_rect.centerx - enter_text.get_width()//2,
                                 enter_rect.centery - enter_text.get_height()//2))

    if message:
        msg_surface = SMALL_FONT.render(message[:80], True, RED if "Error" in message else WHITE)
        screen.blit(msg_surface, (20, HEIGHT - 60))

    pygame.display.flip()

def get_points_from_file():
    try:
        with open(POINTS_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def update_points(username):
    global message
    try:
        new_points = get_points_from_file()
        if new_points == 0:
            message = "No points to extract!"
            print("No points in points.txt")
            return

        response = requests.post(API_URL, data={"username": username, "points": new_points})

        try:
            res = response.json()
        except Exception:
            print("----- SERVER RAW RESPONSE -----")
            print(response.text)
            print("-------------------------------")
            message = "Error: Non-JSON response (see terminal)"
            return

        if res.get("status") == "success":
            message = f"{username} now has {res['new_points']} points!"
            print("✅ Success:", res)
            with open(POINTS_FILE, "w") as f:
                f.write("0")
            print("✅ points.txt cleared")
        else:
            message = f"Error: {res.get('message', 'Unknown error')}"
            print("❌ Server error:", res)

    except Exception as e:
        message = f"Error: {e}"
        print("❌ Exception:", e)

def main():
    global input_active, input_text
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    input_active = True
                    input_text = ""
                elif enter_rect.collidepoint(event.pos) and input_active:
                    update_points(input_text.strip())
                    input_active = False
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    update_points(input_text.strip())
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        draw()
        clock.tick(30)

if __name__ == "__main__":
    main()
