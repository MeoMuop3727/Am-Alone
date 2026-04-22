import pygame, sys, traceback
from packages.components import *

def quit_game():
    pygame.quit()
    sys.exit()

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("main.py")

time = pygame.time.Clock()



while True:
    screen.fill("#FFFFFF")
    events = pygame.event.get()
    time.tick(60)

    for event in events:
        if event.type == pygame.QUIT:
            quit_game()
    
    

    pygame.display.update()

