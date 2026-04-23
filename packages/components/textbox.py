import pygame
from packages.utils.utils_math import minus_tuple, plus_tuple, multi_tuple, INT_MAX
from typing import Tuple, Optional

class TextBox:

    """
        TextBox component for rendering read-only text in a Pygame surface.

        Parameters
        ----------
        surface : pygame.Surface
            Target surface where the TextBox will be rendered.

        content : Optional[str]
            Text content to display. Defaults to empty string if None.

        font : Optional[pygame.font.Font]
            Font object used for rendering text. If None, a font should be created using font_size.

        text_color : Tuple[int, int, int] | str
            Text color in RGB tuple or hex string format.

        antialias : bool
            Whether to apply anti-aliasing when rendering text.

        pos : Tuple[int, int]
            Top-left position (x, y) of the TextBox.

        size : Tuple[int, int]
            Dimensions (width, height) of the TextBox.

        background_color : Tuple[int, int, int] | str
            Background color of the TextBox.

        border_color : Tuple[int, int, int] | str
            Border color of the TextBox.

        border_width : int
            Border thickness. Set to 0 for no border.

        border_radius : int
            Radius for rounded corners.

        padding : int
            Inner spacing. Can be a single integer or a tuple (left, top, right, bottom).

        line_height : int
            Vertical spacing between lines. If 0, defaults to font metrics.

        visible : bool
            Whether the TextBox should be rendered.
    """

    def __init__(self,
                 surface: pygame.Surface,
                 content: Optional[str] = None,
                 font: Optional[pygame.font.Font] = None,
                 text_color: Tuple[int,int,int] | str = "#333333",
                 antialias: bool = True,
                 pos: Tuple[int,int] = (0,0),
                 size: Tuple[int,int] = (500, 200),
                 background_color: Tuple[int,int,int] | str = "#F0F0F0",
                 border_color: Tuple[int,int,int] | str = "#000000",
                 border_width: int = 0,
                 border_radius: int = 0,
                 padding: int = 0,
                 line_height: int = 0,
                 visible: bool = True) -> None:
        self._surface = surface

        # ===== Core =====
        self._content = "" if content is None else content
        self._font = font if font is not None else pygame.font.SysFont(None, 20)
        self._text_color = text_color
        self._antialias = antialias

        # ===== Layout =====
        self._pos = pos
        self._size = size
        self._rect = pygame.Rect(pos, size)

        # ===== Style =====
        self._background_color = background_color
        self._border_color = border_color
        self._border_width = (border_width, border_width)
        self._border_radius = border_radius


        self._padding = padding

        # ===== Text behavior =====
        self._line_height = line_height

        # ===== State =====
        self._visible = visible

    # --- Public API ---
    def update(self) -> None:
        try:
            if self._visible:
                self._draw_border()
                self._draw_background()
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

    def _draw_background(self) -> None:
        background = pygame.Rect(self._pos, self._size)
        pygame.draw.rect(self._surface, self._background_color, background, border_radius=self._border_radius)

    def _draw_content(self) -> None:
        contents = self._content.split()
        line = 0
        length = 0

        padding = self._padding
        max_width = self._size[0] - 2 * padding
        line_height = self._line_height or self._font.get_height()

        for _, text in enumerate(contents):
            text_surface = self._font.render(text, self._antialias, self._text_color)

            if length + text_surface.get_width() > max_width:
                line += 1
                length = 0

            x = self._pos[0] + padding + length
            y = self._pos[1] + padding + line * line_height

            self._surface.blit(text_surface, (x, y))
            
            length += text_surface.get_width() + 5

    
