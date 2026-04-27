import pygame
from packages.systems.manager_scences import ScenceManager
from packages.scences.game import *

pygame.init()

screen = pygame.display.set_mode((1280,720))

manager = ScenceManager(screen)

manager.push_scence(PlayGame(screen))

manager.run()
