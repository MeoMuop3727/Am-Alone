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
        Button component for interactive UI in Pygame.

        This Button supports multiple visual states (normal, hover, pressed, disabled),
        custom colors, optional sound feedback, and click callbacks.

        Parameters
        ----------
        surface : pygame.Surface
            Target surface where the Button will be rendered.

        pos : Tuple[int, int]
            Top-left position (x, y) of the Button.

        size : Tuple[int, int]
            Dimensions (width, height) of the Button.

        content : Optional[str]
            Text displayed on the Button.

        font : pygame.font.Font
            Font used to render the button text.

        text_color : Tuple[int, int, int] | str
            Text color in normal state.

        text_color_hover : Tuple[int, int, int] | str
            Text color when the mouse is hovering over the button.

        text_color_pressed : Tuple[int, int, int] | str
            Text color when the button is being pressed.

        text_color_disabled : Tuple[int, int, int] | str
            Text color when the button is disabled.

        color_normal : Tuple[int, int, int] | str
            Background color in normal state.

        color_hover : Tuple[int, int, int] | str
            Background color when hovered.

        color_pressed : Tuple[int, int, int] | str
            Background color when pressed.

        color_disabled : Tuple[int, int, int] | str
            Background color when disabled.

        on_click : Optional[Callable[[], None]]
            Callback function executed when the button is clicked.

        border_width : int
            Width of the button border. Set to 0 for no border.

        border_radius : int
            Radius for rounded corners.

        border_color : Tuple[int, int, int] | str
            Border color in normal state.

        border_color_hover : Tuple[int, int, int] | str
            Border color when hovered.

        border_color_pressed : Tuple[int, int, int] | str
            Border color when pressed.

        border_color_disabled : Tuple[int, int, int] | str
            Border color when disabled.

        sound_click : Optional[pygame.mixer.Sound]
            Sound played when the button is clicked.

        disabled : bool
            If True, the button is inactive and ignores user input.
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
        self._rect = pygame.Rect(pos, size)
        
        self._pos = pos
        self._size = size

        self._content = "" if content is None else content
        self._font = font if font is not None else pygame.font.SysFont(None, 20)
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
        rect = self._rect

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

