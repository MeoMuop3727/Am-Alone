import pygame
from packages.systems.manager_scences import Scene
from typing import Optional
from packages.components import *

class PlayGame(Scene):
    def __init__(self, 
                 surface: pygame.Surface,
                 font_style: Optional[str] = None):
        super().__init__()

        self._screen = surface
        self._size = self._screen.get_size()

        self._font = pygame.font.Font(font_style, 50)

        self._value = 0

        self._size_button_paused = (50,50)
        self._padding = (10,10)
        self._button_paused = ButtonText(
            surface=self._screen,
            pos=(
                self._size[0] - self._size_button_paused[0] - self._padding[0],
                self._padding[1]
            ),
            size=self._size_button_paused,
            content="||",
            color_normal="#BF092F",
            color_hover="#FE7F2D",
            color_pressed="#F4853B",
            text_color="#EEEEEE",
            text_color_hover="#333333",
            text_color_pressed="#222222",
            on_click=None,
            font=pygame.font.SysFont(None, 40)
        )
    
    def render(self, screen):
        screen.fill("#FFFFFF")
        
        text_surface = self._font.render(str(self._value), True, "#333333")
        text_rect = text_surface.get_rect(center=(
            self._size[0]// 2,
            30
        ))

        screen.blit(text_surface, text_rect)

        self._button_paused.update()
    
    