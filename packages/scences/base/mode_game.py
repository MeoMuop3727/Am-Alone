import pygame
from packages.systems.manager_scences import Scene
from packages.components import *
from typing import Optional
from packages.utils.utils_math import minus_tuple

class ModeGame(Scene):
    def __init__(self, 
                 surface: pygame.Surface,
                 font_style: Optional[str] = None):
        super().__init__()

        self._surface = surface
        self._size = surface.get_size()

        self._font_text = pygame.font.Font(font_style, 37)

        self._content = "Unvalible"

        self._size_button = (50,50)
        self._padding = (10,10)
        self._button = ButtonText(
            surface=self._surface,
            content="x",
            size=self._size_button,
            pos=(
                self._size[0] - self._size_button[0] - self._padding[0],
                self._padding[1]
            ),
            color_normal="#C3110C",
            color_hover="#E6501B",
            color_pressed="#E6501B",
            text_color="#333333",
            text_color_hover="#FFFFFF",
            text_color_pressed="#FFFFFF",
            on_click=lambda: self._switch(),
            font=pygame.font.SysFont(None, 40)
        )

    def render(self, screen):
        screen.fill("#FFFFFF")

        text_surface = TextBox(
            surface=screen,
            content=self._content,
            size=minus_tuple(screen.get_size(), (self._size_button[0] * 2, 0)),
            padding=10,
            line_height=27,
            background_color="#FFFFFF",
            font=self._font_text
        )

        text_surface.update()
        self._button.update()
    
    def _switch(self) -> None:
        self.manager.pop_scence()