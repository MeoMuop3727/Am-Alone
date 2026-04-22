import pygame
from typing import Tuple, Optional, Callable
from enum import Enum
from packages.utils.utils_math import minus_tuple, plus_tuple, multi_tuple

class ButtonStates(Enum):
    NORMAL = 1
    HOVER = 2
    PRESSED = 3
    DISABLED = 4

class ButtonText:

    """
        A reusable, styled button component for pygame UI.
 
        Supports hover, press, disabled states, and a callback fired on click release.

        Args:
            surface:    Screen to draw the button
            pos:        (x,y) position (top-left)
            size:       (width, height) in pixels
            content:    Text display on the button (None = "")
            font:       Font family (None = font default of pygame)
            text_color: Color of text on the button (Normal)
            text_color_hover:   Color of text on the button when hover
            text_color_pressed: Color of text on the button when pressed
            text_color_disabled:    Color of text on the button when disabled
            color_normal:   Background color (R, B, G)
            color_hover:    Background color on hover
            color_pressed:  Background color on pressed
            color_disable:  Background color on disable
            on_click:   Callback function called when the button is clicked
            border_width:   Outline thickness (0 = no border)
            border_radius:  Corner rounding in pixels
            border_color:   Outline color
            border_color_hover: Outline color hover
            border_color_pressed: Outline color pressed
            border_color_disabled: Outlinr color disabled
            sound_click:    The sound when the button is clicked
    """
    
    def __init__(self,
                 surface: pygame.Surface,
                 pos: Tuple[int,int] = (0,0),
                 size: Tuple[int,int] = (200, 65),
                 content: Optional[str] = None,
                 font: pygame.font.Font = None,
                 text_color: Tuple[int,int,int] | str = "#F0F0F0",
                 text_color_hover: Tuple[int,int,int] | str = "#37353E",
                 text_color_pressed: Tuple[int,int,int] | str = "#37353E",
                 text_color_disabled: Tuple[int,int,int] | str = "#37353E",
                 color_normal: Tuple[int,int,int] | str = "#37353E",
                 color_hover: Tuple[int,int,int] | str = "#F0F0F0",
                 color_pressed: Tuple[int,int,int] | str = "#F0F0F0",
                 color_disabled: Tuple[int,int,int] | str = "#F0F0F0",
                 on_click: Optional[Callable[[], None]] = None,
                 border_width: int = 0,
                 border_radius: int = 0,
                 border_color: Tuple[int,int,int] | str = "#000000",
                 border_color_hover: Tuple[int,int,int] | str = "#000000",
                 border_color_pressed: Tuple[int,int,int] | str = "#000000",
                 border_color_disabled: Tuple[int,int,int] | str = "#000000",
                 sound_click: Optional[pygame.mixer.Sound] = None,
                 disabled: bool = False) -> None:
        self._surface = surface
        self._pos = pos
        self._size = size

        self._content = content or ""
        self._font = font or pygame.font.SysFont("serif", 20)
        self._text_color = text_color
        self._text_color_hover = text_color_hover
        self._text_color_pressed = text_color_pressed
        self._text_color_disabled = text_color_disabled

        self._color_normal = color_normal
        self._color_hover = color_hover
        self._color_pressed = color_pressed
        self._color_disabled = color_disabled

        self._on_click = on_click

        self._border_width = border_width
        self._border_radius = border_radius
        self._border_color = border_color
        self._border_color_hover = border_color_hover
        self._border_color_pressed = border_color_pressed
        self._border_color_disabled = border_color_disabled

        self._sound_click = sound_click
    
        self._state = ButtonStates.DISABLED if disabled else ButtonStates.NORMAL
        self._hovered = False
        self._pressed = False


    # --- Pulic API ---
    @property
    def disabled(self) -> bool:
        return self._state == ButtonStates.DISABLED
    
    @disabled.setter
    def disabled(self, value: bool) -> None:
        self._state = ButtonStates.DISABLED if value else ButtonStates.NORMAL

    @property
    def hovered(self) -> bool:
        return self._hovered

    @property
    def pressed(self) -> bool:
        return self._pressed

    def update(self) -> None:
        try:
            rect = pygame.Rect(self._pos, self._size)
            mouse_pos = pygame.mouse.get_pos()

            if self._state == ButtonStates.DISABLED:
                self._pressed = False
                self._hovered = False
            
            self._hovered = rect.collidepoint(mouse_pos) # Update hover

            if self._hovered and pygame.mouse.get_pressed()[0]:
                if not self._pressed:
                    self._pressed = True
            else:
                if self._pressed and self._hovered:
                    try:
                        if self._on_click: self._on_click()
                        if self._sound_click(): self._sound_click.play()
                    except TypeError: pass
                self._pressed = False             

            visual_state = self._get_visual_state()       

            color_button = self._set_color_button(visual_state)
            color_content = self._set_color_content(visual_state)
            color_border = self._set_color_border(visual_state)

            self._draw_border(color_border)
            self._draw_button(color_button)
            self._draw_content(color_content)
        except Exception:
            import traceback
            traceback.print_exc()

    # --- Rendering ---
    def _draw_button(self, color: Tuple[int,int,int] | str) -> None:
        button = pygame.Rect(self._pos, self._size)

        pygame.draw.rect(self._surface, color, button, border_radius=self._border_radius)

    def _draw_content(self, color: Tuple[int,int,int] | str) -> None:
        rect = pygame.Rect(self._pos, self._size)

        text_surface = self._font.render(self._content, True, color)
        text_rect = text_surface.get_rect(center=rect.center)

        self._surface.blit(text_surface, text_rect)
    
    def _draw_border(self, color: Tuple[int,int,int] | str) -> None: 
        border_width = (self._border_width, self._border_width)
        border = pygame.Rect(
            minus_tuple(self._pos, border_width),
            plus_tuple(self._size, multi_tuple(border_width, (2,2)))
        )

        pygame.draw.rect(self._surface, color, border, border_radius=self._border_radius)

    def _set_color_content(self, state: ButtonStates) -> Tuple[int,int,int] | str:
        if state == ButtonStates.NORMAL: return self._text_color
        elif state == ButtonStates.PRESSED: return self._text_color_pressed
        elif state == ButtonStates.HOVER: return self._text_color_hover
        else: return self._text_color_disabled

    def _set_color_button(self, state: ButtonStates) -> Tuple[int,int,int] | str:
        if state == ButtonStates.NORMAL: return self._color_normal
        elif state == ButtonStates.PRESSED: return self._color_pressed
        elif state == ButtonStates.HOVER: return self._color_hover
        else: return self._color_disabled

    def _set_color_border(self, state: ButtonStates) -> Tuple[int,int,int] | str:
        if state == ButtonStates.NORMAL: return self._border_color
        elif state == ButtonStates.PRESSED: return self._border_color_pressed
        elif state == ButtonStates.HOVER: return self._border_color_hover
        else: return self._border_color_disabled

    def _get_visual_state(self) -> ButtonStates:
        if self._state == ButtonStates.DISABLED:
            return ButtonStates.DISABLED
        if self._pressed:
            return ButtonStates.PRESSED
        if self._hovered:
            return ButtonStates.HOVER
        return ButtonStates.NORMAL

