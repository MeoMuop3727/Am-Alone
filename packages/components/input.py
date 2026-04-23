import pygame
from typing import Tuple, Optional, Callable
from packages.utils.utils_math import INT_MAX, minus_tuple, plus_tuple, multi_tuple
from enum import Enum

class InputStates(Enum):
    NORMAL = 1
    ACTIVE = 2
    HOVER = 3

class Input:
    def __init__(self,
                 surface: pygame.Surface,
                 font: Optional[pygame.font.Font] = None,
                 value: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 max_length: int = INT_MAX,
                 cursor_visible: bool = True,
                 cursor_timer: float = 0.0,
                 cursor_interval: float = 0.5,
                 disabled: bool = False,
                 size: Tuple[int,int] = (350, 65),
                 pos: Tuple[int,int] = (0,0),
                 text_color: Tuple[int,int,int] | str = "#333333",
                 placeholder_color: Tuple[int,int,int] | str = "#555555",
                 background_color: Tuple[int,int,int] | str = "#F0F0F0",
                 background_color_hover: Tuple[int,int,int] | str = "#F0F0F0",
                 background_color_active: Tuple[int,int,int] | str = "#F0F0F0",
                 border_color: Tuple[int,int,int] | str = "#000000",
                 border_width: int = 0,
                 border_radius: int = 0,
                 allow_numbers: bool = True,
                 allow_letters: bool = True,
                 allow_special: bool = True,
                 password_mode: bool = False,
                 on_submit: Callable[[str], None] = None,
                 on_change: Callable[[str], None] = None) -> None:
        # ===== Surface =====
        self._surface = surface

        # ===== Data =====
        self._text = "" if value is None else value
        self._placeholder = "" if placeholder is None else placeholder
        self._font = font if font is not None else pygame.font.SysFont(None, 20)
        self._max_length = max_length

        # ===== Cursor =====
        self._cursor_visible = cursor_visible
        self._cursor_timer = cursor_timer
        self._cursor_interval = cursor_interval
        self._cursor_pos = (len(self._text), pos[1])

        # ===== State =====
        self._disabled = disabled
        self._is_focused = False
        self._is_hovered = False

        # ===== Layout =====
        self._size = size
        self._pos = pos
        self._rect = pygame.Rect(pos, size)

        # ===== Colors  =====
        self._text_color = text_color
        self._placeholder_color = placeholder_color

        self._bg_color = background_color
        self._bg_color_hover = background_color_hover
        self._bg_color_active = background_color_active

        self._border_color = border_color
        self._border_width = (border_width, border_width)
        self._border_radius = border_radius

        # ===== Input rules =====
        self._allow_numbers = allow_numbers
        self._allow_letters = allow_letters
        self._allow_special = allow_special
        self._password_mode = password_mode

        # ===== Callbacks =====
        self._on_submit = on_submit
        self._on_change = on_change

        self._state = InputStates.NORMAL
        self._is_hover = False
        self._is_active = False

    # --- Pulic API ---
    @property
    def content(self) -> str:
        return self._text
    
    def update(self, event: pygame.event.Event) -> None:
        try:
            if not self._disabled:
                visual_state = self._get_visual_state()

                self._input(event)

                self._draw_border()
                self._draw_background(visual_state)
                self._draw_cursor()
                self._draw_content()
        except Exception as e:
            import traceback
            traceback.print_exc()

    # --- Rendering ---
    def _draw_border(self) -> None:
        border = pygame.Rect(
            minus_tuple(self._pos, self._border_width),
            plus_tuple(self._size, multi_tuple(self._border_width, (2,2)))
        )

        pygame.draw.rect(self._surface, self._border_color, border, border_radius=self._border_radius)

    def _draw_background(self, state: InputStates) -> None:
        color = self._set_background_color(state)
        background = pygame.Rect(self._pos, self._size)

        pygame.draw.rect(self._surface, color, background, border_radius=self._border_radius)

    def _draw_content(self) -> None:
        if self._password_mode:
            contents = len(self._text) * "*"
        else:
            contents = self._text.split()

        line = 0
        length = 0

        padding = 5
        max_width = self._size[0] - 2 * padding
        line_height = self._line_height or self._font.get_height()

        for _, text in enumerate(contents):
            text_surface = self._font.render(text, True, self._text_color)

            if length + text_surface.get_width() > max_width:
                line += 1
                length = 0

            x = self._pos[0] + padding + length
            y = self._pos[1] + padding + line * line_height

            self._surface.blit(text_surface, (x, y))
            
            length += text_surface.get_width() + 5
    
    def _draw_cursor(self) -> None:
        pass

    # --- Input ---
    def _input(self, event: pygame.event.Event) -> None:
        pass
    
    # --- Set up ---
    def _set_background_color(self, state: InputStates) -> Tuple[int,int,int] | str:
        if state == InputStates.NORMAL:
            return self._bg_color
        elif state == InputStates.HOVER:
            return self._bg_color_hover
        else:
            return self._bg_color_active

    def _get_visual_state(self) -> InputStates:
        if self._is_hover:
            return InputStates.HOVER
        elif self._is_active:
            return InputStates.ACTIVE
        return InputStates.NORMAL
    