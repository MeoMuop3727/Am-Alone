import pygame, sys
from packages.components import *

pygame.init()

screen = pygame.display.set_mode((1280,720))

pygame.display.set_caption("Test components")

while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()