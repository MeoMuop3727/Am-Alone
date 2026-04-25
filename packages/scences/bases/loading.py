import pygame
from typing import Optional, Tuple

class LoadingScence:
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


