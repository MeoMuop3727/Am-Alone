import pygame
from packages.systems.manager_scences import Scene
from typing import Optional
from packages.components import *
from packages.utils.utils_math import multi_tuple

from .paused import PauseGame
class PlayGame(Scene):
    def __init__(self, 
                 surface: pygame.Surface,
                 font_style: Optional[str] = None):
        super().__init__()

        self._screen = surface
        self._size = surface.get_size()

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
            on_click=lambda: self._switch(),
            font=pygame.font.SysFont(None, 40)
        )

        self._image_original = pygame.image.load("packages/assets/images/default/image.png").convert_alpha()
        self._scale = 0.5
        self._image = pygame.transform.scale(self._image_original, multi_tuple(self._image_original.get_size(), (self._scale, self._scale)))
        self._rect = self._image.get_rect(center=(self._size[0] // 2, self._size[1] // 2))

        self._sound = pygame.mixer.Sound("packages/assets/sounds/default/sound.mp3")

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self._rect.collidepoint(mouse_pos)

        if hovered:
            self._scale = 0.65
            if pygame.mouse.get_pressed()[0]:
                self._scale = 0.5
                self._sound.play()
        else:
            self._scale = 0.5      
        
        self._update_image_scale()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hovered:
                self._value += 1

    def render(self, screen):
        screen.fill("#FFFFFF")

        text_surface = self._font.render(str(self._value), True, "#333333")
        text_rect = text_surface.get_rect(center=(
            self._size[0]// 2,
            30
        ))

        screen.blit(text_surface, text_rect)

        self._button_paused.update()

        screen.blit(self._image, self._rect)
    
    def _update_image_scale(self):
        new_size = multi_tuple(
            self._image_original.get_size(),
            (self._scale, self._scale)
        )

        self._image = pygame.transform.scale(
            self._image_original,
            new_size
        )

        self._rect = self._image.get_rect(
            center=(self._size[0] // 2, self._size[1] // 2)
        )
    
    def get_score(self) -> int:
        return self._value
    
    def _switch(self):
        self.manager.push_scence(PauseGame(self._value, self._screen))
    
    