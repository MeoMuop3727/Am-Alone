import pygame
from typing import Tuple, Optional
from packages.utils.utils_math import INT_MAX, minus_tuple, plus_tuple, multi_tuple
from enum import Enum

class InputStates(Enum):
    NORMAL = 1
    FOCUSED = 2
    HOVERED = 3

class Input:

    """
        InputBox is a customizable text input component for Pygame.

        It supports text entry, cursor management, multi-line wrapping, and basic UI states
        such as hover, focus, and disabled. The component is highly configurable in terms
        of appearance, input behavior, and rendering.

        Parameters
        ----------
        surface : pygame.Surface
            The surface where the input box will be rendered.

        font : pygame.font.Font, optional
            Font used to render the text. If None, a default font should be provided.

        value : str, optional
            Initial text value of the input box.

        placeholder : str, optional
            Placeholder text displayed when the input is empty.

        max_length : int
            Maximum number of characters allowed in the input.

        cursor_interval : float
            Time interval (in seconds) for cursor blinking.

        disabled : bool
            If True, the input box is non-interactive.

        size : Tuple[int, int]
            Dimensions of the input box (width, height).

        pos : Tuple[int, int]
            Top-left position of the input box on the surface.

        text_color : Tuple[int, int, int] | str
            Color of the input text (RGB tuple or hex string).

        placeholder_color : Tuple[int, int, int] | str
            Color of the placeholder text.

        background_color : Tuple[int, int, int] | str
            Default background color.

        background_color_hover : Tuple[int, int, int] | str
            Background color when the mouse hovers over the input box.

        background_color_focused : Tuple[int, int, int] | str
            Background color when the input box is focused.

        border_color : Tuple[int, int, int] | str
            Color of the border.

        border_width : int
            Width of the border. Set to 0 for no border.

        border_radius : int
            Radius for rounded corners.

        allow_numbers : bool
            Whether numeric input (0 - 9) is allowed.

        allow_letters : bool
            Whether alphabetic input (a - z, A - Z) is allowed.

        allow_special : bool
            Whether special characters are allowed.

        password_mode : bool
            If True, the input text is masked (e.g., displayed as '*').

        line_height : int
            Additional vertical spacing between lines for multi-line text rendering.
    """

    def __init__(self,
                 surface: pygame.Surface,
                 font: Optional[pygame.font.Font] = None,
                 value: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 max_length: int = INT_MAX,
                 cursor_interval: float = 0.5,
                 disabled: bool = False,
                 size: Tuple[int,int] = (350, 65),
                 pos: Tuple[int,int] = (0,0),
                 text_color: Tuple[int,int,int] | str = "#333333",
                 placeholder_color: Tuple[int,int,int] | str = "#555555",
                 background_color: Tuple[int,int,int] | str = "#F0F0F0",
                 background_color_hover: Tuple[int,int,int] | str = "#F0F0F0",
                 background_color_focused: Tuple[int,int,int] | str = "#F0F0F0",
                 border_color: Tuple[int,int,int] | str = "#000000",
                 border_width: int = 0,
                 border_radius: int = 0,
                 allow_numbers: bool = True,
                 allow_letters: bool = True,
                 allow_special: bool = True,
                 password_mode: bool = False,
                 line_height: int = 5) -> None:
        # ===== Surface =====
        self._surface = surface

        # ===== Data =====
        self._text = "" if value is None else value
        self._placeholder = "" if placeholder is None else placeholder
        self._font = font if font is not None else pygame.font.SysFont(None, 20)
        self._max_length = max_length

        # ===== Cursor =====
        self._cursor_visible = False
        self._cursor_timer = 0
        self._cursor_interval = cursor_interval
        self._cursor_pos = len(self._text)

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
        self._line_height = line_height

        self._bg_color = background_color
        self._bg_color_hover = background_color_hover
        self._bg_color_focused = background_color_focused

        self._border_color = border_color
        self._border_width = (border_width, border_width)
        self._border_radius = border_radius

        # ===== Input rules =====
        self._allow_numbers = allow_numbers
        self._allow_letters = allow_letters
        self._allow_special = allow_special
        self._password_mode = password_mode

        self._state = InputStates.NORMAL
        self._padding = 5
        self._max_width = size[0] - 2 * self._padding

    # --- Pulic API ---
    @property
    def content(self) -> str:
        return self._text
    
    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()
        try:
            if not self._disabled:
                self._is_hovered = self._rect.collidepoint(mouse_pos)

                if self._is_hovered and pygame.mouse.get_pressed()[0]:
                    if not self._is_focused:
                        self._is_focused = True
                elif not self._is_hovered and pygame.mouse.get_pressed()[0]:
                    if self._is_focused:
                        self._is_focused = False
                        self._cursor_visible = False
                
                if self._is_focused:
                    if now - self._cursor_timer > self._cursor_interval * 1e3:
                        self._cursor_visible = not self._cursor_visible
                        self._cursor_timer = now

                visual_state = self._get_visual_state()

                self._draw_border()
                self._draw_background(visual_state)
                self._draw_content()

                if self._cursor_visible:
                    self._draw_cursor()
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
        # if self._password_mode:
        #     contents = len(self._text) * "*"
        # else:
        #     contents = self._text.split()

        # line = 0
        # length = 0

        # padding = self._padding
        # max_width = self._size[0] - 2 * padding
        # line_height = self._line_height or self._font.get_height()

        # for _, text in enumerate(contents):
        #     text_surface = self._font.render(text, True, self._text_color)

        #     if length + text_surface.get_width() > max_width:
        #         line += 1
        #         length = 0

        #     x = self._pos[0] + padding + length
        #     y = self._pos[1] + padding + line * line_height

        #     self._surface.blit(text_surface, (x, y))
            
        #     length += text_surface.get_width() + 5

        lines = self._wrap_text(self._text)

        y = self._pos[1] + self._padding

        for line in lines:
            surface = self._font.render(line, True, self._text_color)
            self._surface.blit(surface, (self._pos[0] + self._padding, y))

            y += self._font.get_height() + self._line_height
    
    def _draw_cursor(self) -> None:
        # WIDTH_CURSOR = 4
        # MAX_WIDTH = self._size[0] - 2 * self._padding

        # text_before = self._text[:self._cursor_pos]

        # lines = []
        # current_line = ""

        # # ===== Wrap text thủ công =====
        # for char in text_before:
        #     test_line = current_line + char
        #     if self._font.size(test_line)[0] <= MAX_WIDTH:
        #         current_line = test_line
        #     else:
        #         lines.append(current_line)
        #         current_line = char

        # lines.append(current_line)

        # # ===== Determinate the pos of cursor =====
        # cursor_line = len(lines) - 1
        # cursor_col_text = lines[-1]

        # cursor_x_offset = self._font.size(cursor_col_text)[0]
        # cursor_y_offset = cursor_line * (self._font.get_height() + self._line_height)

        # x = self._pos[0] + self._padding + cursor_x_offset
        # y = self._pos[1] + self._padding + cursor_y_offset

        # cursor = pygame.Rect(
        #     (x, y),
        #     (WIDTH_CURSOR, self._font.get_height())
        # )

        # pygame.draw.rect(self._surface, self._text_color, cursor)

        WIDTH_CURSOR = 4

        text_before = self._text[:self._cursor_pos]
        lines = self._wrap_text(text_before)

        cursor_line = len(lines) - 1
        cursor_col_text = lines[-1]

        cursor_x = self._font.size(cursor_col_text)[0]
        cursor_y = cursor_line * (self._font.get_height() + self._line_height)

        x = self._pos[0] + self._padding + cursor_x
        y = self._pos[1] + self._padding + cursor_y

        cursor = pygame.Rect(
            (x, y),
            (WIDTH_CURSOR, self._font.get_height())
        )

        pygame.draw.rect(self._surface, self._text_color, cursor)

    # --- Input ---
    def input(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN: return
        if not self._is_focused or self._disabled: return 

        # ===== Backspace =====
        if event.key == pygame.K_BACKSPACE:
            if self._cursor_pos > 0:
                self._text = self._text[:self._cursor_pos - 1] + self._text[self._cursor_pos:] 
                self._cursor_pos -= 1

        # ===== Space =====
        elif event.key == pygame.K_SPACE:
            self._insert_char(" ")

        # ===== Change the cursor pos =====
        elif event.key == pygame.K_LEFT:
            self._cursor_pos = max(0, self._cursor_pos - 1)
        elif event.key == pygame.K_RIGHT:
            self._cursor_pos = min(len(self._text), self._cursor_pos + 1)

        # ===== Normal char =====
        elif event.unicode:
            self._insert_char(event.unicode)
    
    # --- Set up ---
    def _wrap_text(self, text: str):
        lines = []
        current = ""

        for char in text:
            if self._font.size(current + char)[0] <= self._max_width:
                current += char
            else:
                lines.append(current)
                current = char

        lines.append(current)
        return lines

    def _is_char_valid(self, char: Optional[str] = None) -> bool:
        if char.isdigit():
            return self._allow_numbers
        elif char.isalpha():
            return self._allow_letters
        return self._allow_special
    
    def _insert_char(self, char: Optional[str] = None) -> None:
        if not char: return
        if len(self._text) >= self._max_length: return
        if not self._is_char_valid(char): return

        self._text = self._text[:self._cursor_pos] + char + self._text[self._cursor_pos:]
        self._cursor_pos += 1

    def _set_background_color(self, state: InputStates) -> Tuple[int,int,int] | str:
        if state == InputStates.NORMAL:
            return self._bg_color
        elif state == InputStates.HOVERED:
            return self._bg_color_hover
        else:
            return self._bg_color_focused

    def _get_visual_state(self) -> InputStates:
        if self._is_hovered:
            return InputStates.HOVERED
        elif self._is_focused:
            return InputStates.FOCUSED
        return InputStates.NORMAL
    