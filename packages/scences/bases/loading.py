import pygame
from typing import Optional, Tuple

class LoadingScence:

    """
        Initialize a loading scene component used for displaying animated loading text.

        Args:
            surface (pygame.Surface):
                The main surface where the loading scene will be rendered.

            background_color (Tuple[int, int, int] | str, optional):
                Background color of the loading scene. Can be an RGB tuple
                or a hex string (e.g., "#000000"). Defaults to black.

            size (Tuple[int, int], optional):
                Size (width, height) of the loading area. If (0, 0),
                it should typically fallback to the surface size.

            pos (Tuple[int, int], optional):
                Top-left position of the loading scene relative to the surface.

            font (Optional[pygame.font.Font], optional):
                Font used to render the loading text. If None, a default font
                should be assigned internally.

            time_interval (float, optional):
                Time interval (in seconds) between animation updates
                (e.g., blinking dots "..."). Defaults to 0.5.

            text_color (Tuple[int, int, int] | str, optional):
                Color of the loading text. Accepts RGB tuple or hex string.
                Defaults to white.

            padding (int, optional):
                Inner padding applied when positioning text inside the scene.
    """

    def __init__(self,
                 surface: pygame.Surface,
                 background_color: Tuple[int,int,int] | str = "#000000",
                 size: Tuple[int,int] = (0,0),
                 pos: Tuple[int,int] = (0,0),
                 font: Optional[pygame.font.Font] = None,
                 time_interval: float = 0.5,
                 text_color: Tuple[int,int,int] | str = "#FFFFFF",
                 padding: int = 10) -> None:
        # Surface
        self._surface = surface
        self._rect = pygame.Rect(pos, size)

        # Set up
        self._size = size
        self._pos = pos

        # Background color
        self._background_color = background_color

        # Text
        self._font = font if font is not None else pygame.font.SysFont(None, 20)
        self._text_color = text_color

        # Set up animation
        self._time = 0
        self._time_interval = time_interval
        self._docts = 0

        # Padding
        self._padding = padding # Fix pos of text

    # --- Public API ---
    @property
    def surface(self) -> pygame.Rect:
        return self._rect
    
    def update(self) -> None:
        try:
            self._draw_frame()
            self._draw_text()
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    # --- Rendering ---
    def _draw_frame(self) -> None:
        frame = self._rect
        pygame.draw.rect(self._surface, self._background_color, frame)

    
    def _draw_text(self) -> None:
        now = pygame.time.get_ticks()
        if now - self._time >= self._time_interval * 1e3:
            self._docts = (self._docts + 1) % 4 # 0 -> 3
            self._time = now
        
        text = "Loading" + "." * self._docts

        text_surface = self._font.render(text, True, self._text_color)
        text_rect = text_surface.get_rect(center=(
            self._size[0] - self._font.size(text)[0] // 2 - self._padding,
            self._size[1] - self._font.get_height() // 2 - self._padding
        ))

        self._surface.blit(text_surface, text_rect)


