import os
os.environ["SDL_AUDIODRIVER"] = "pulseaudio"

import pygame
from packages.systems.manager_scences import ScenceManager
from packages.scences.base.main_menu import MainMenu
from packages.scences.game import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280,720))

manager = ScenceManager(screen)

manager.push_scence(MainMenu(screen))

manager.run()
