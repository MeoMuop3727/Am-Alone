from packages.systems.manager_scences import ScenceManager
from packages.scences.base import *
import pygame

pygame.init()

screen = pygame.display.set_mode((1280,720))

manager = ScenceManager(screen)
manager.push_scence(MainMenu(screen))

manager.run()
