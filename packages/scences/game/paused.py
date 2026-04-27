import pygame
from packages.systems.manager_scences import Scene
from typing import Optional
from packages.components import *

class PauseGame(Scene):
    def __init__(self, 
                 score: int,
                 surface: pygame.Surface,
                 font_style: Optional[str] = None):
        super().__init__()

        self._surface = surface

        self._font = pygame.font.Font(font_style, 60)

        self._score = score

        self._size = surface.get_size()

        self._list_buttons: list[ButtonText] = []
        self._draw_button()

    def _draw_button(self) -> None:
        buttons = ["CONTINUE", "QUIT"]

        funcs = [
            lambda: self.manager.pop_scence(),
            None
        ]

        SIZE_BUTTON = (250, 80)

        for i, button_label in enumerate(buttons):
            button = ButtonText(
                surface=self._surface,
                content=button_label,
                font=self._font,
                pos=(
                    (self._size[0] - SIZE_BUTTON[0]) // 2,
                    self._size[1] // 2 + (SIZE_BUTTON[1] + 20) * i
                ),
                on_click=funcs[i],
                size=SIZE_BUTTON
            )

            self._list_buttons.append(button)

    def render(self, screen):
        screen.fill("#8A868645")

        paused = self._font.render("PAUSED GAME", True, "#FFFFFF")
        paused_rect = paused.get_rect(center=(
            self._size[0] // 2,
            self._size[1] // 2 - 200
        ))

        score = self._font.render("Score: " + str(self._score), True, "#FFFFFF")
        score_rect = score.get_rect(center=(
            self._size[0] // 2,
            self._size[1] // 2 - 100
        ))

        screen.blit(paused, paused_rect)
        screen.blit(score, score_rect)

        for button in self._list_buttons:
            button.update()

    
    