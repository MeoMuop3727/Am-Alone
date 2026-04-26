import pygame
from packages.systems.manager_scences import Scene
from packages.components import *
from typing import Optional

from .information import Information
from .setting import Setting
from .mode_game import ModeGame
from .help import Help

class MainMenu(Scene):
    def __init__(self, 
                 surface: pygame.Surface,
                 font_style: Optional[str] = None):
        super().__init__()

        self._surface = surface

        self._font_title = pygame.font.Font(font_style, 120)
        self._font_press = pygame.font.Font(font_style, 50)
        self._font_note = pygame.font.Font(font_style, 25)

        self._title_visible = True
        self._time = 0
        self._time_interval = 0.5 # Milisecond

        self._list_buttons: list[ButtonText] = []
        self._set_button()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and not event.repeat:
                pass

    def update(self, dt):
        self._time += dt * 0.75
        if self._time >= self._time_interval:
            self._title_visible = not self._title_visible
            self._time = 0

    def render(self, screen):
        screen.fill("#222222") # Clean frame

        size = screen.get_size()

        title = self._font_title.render("TAP-TAP AND BAP-BAP", True, "#FFFFFF")
        title_rect = title.get_rect(center=(
            size[0] // 2,
            size[1] // 2 - 280
        ))

        note = self._font_note.render("The more you clap, the more enthusiastic they become; the more you play, the more fun it gets", True, "#FFFFFF")
        note_rect = note.get_rect(center=(
            size[0] // 2,
            size[1] // 2 - 220
        ))        

        press = self._font_press.render("PRESS ANY BUTTON TO START", True, "#FFFFFF")
        press_rect = press.get_rect(center=(
            size[0] // 2,
            size[1] // 2 + 300
        ))

        if self._title_visible: screen.blit(press, press_rect)
        
        screen.blit(title, title_rect)
        screen.blit(note, note_rect)

        for button in self._list_buttons:
            button.update()
    
    def _set_button(self) -> None:
        buttons = ["H", "S", "M", "I"]
        funcs = [
            lambda: self._switch(Help(self._surface)),
            lambda: self._switch(Setting(self._surface)),
            lambda: self._switch(ModeGame(self._surface)),
            lambda: self._switch(Information(self._surface))
        ]

        PADDING = (10,10)
        SIZE_BUTTON = (30,30)
        GAP_BUTTON = 15

        for i, button_label in enumerate(buttons):
            button = ButtonText(
                surface=self._surface,
                pos=(PADDING[0], PADDING[1] + (SIZE_BUTTON[1] + GAP_BUTTON) * i),
                content=button_label,
                font=pygame.font.SysFont(None, 25),
                color_normal="#F0F0F0",
                color_pressed="#FFFFFF",
                color_hover="#333333",
                text_color="#222222",
                text_color_pressed="#333333",
                text_color_hover="#FFFFFF",
                size=SIZE_BUTTON,
                on_click=funcs[i]
            )
            
            self._list_buttons.append(button)
    
    def _switch(self, scence: Scene) -> None:
        self.manager.push_scence(scence)


