import pygame, sys, json
from packages.components import *

pygame.init()

with open("packages/systems/screen_setting.json") as file:
    config = json.load(file)

# --- Functions Game ---
def quit_game():
    pygame.quit()
    sys.exit()

# --- Set up ---
WIDTH, HEIGHT = config["window"]["width"], config["window"]["height"]
FONT_FAMILY = config["display"]["font_family"]
FPS = config["display"]["fps_limit"]
BACKGROUND_COLOR = config["render"]["background_color"]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(config["display"]["title"])

# --- UI/Scence ---


while True:
    EVENTS = pygame.event.get()

    screen.fill(BACKGROUND_COLOR)

    # --- Rendering ---

    for event in EVENTS:
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and (event.mod and pygame.KMOD_ALT):
                quit_game()
    
    pygame.display.flip()
