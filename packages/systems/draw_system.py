import pygame, numpy
import pygame.surfarray as surfarray
from numpy.typing import NDArray
from typing import Tuple, Optional
from packages.utils.utils_math import multi_tuple

class DrawSystem:
    def __init__(self,
                 surface: pygame.Surface,
                 colors: NDArray[numpy.uint8],
                 matrix: NDArray[numpy.uint8],
                 pos: Tuple[int,int] = (0,0),
                 scale: int = 1,
                 disabled: bool = False):
        # Surface
        self._surface = surface

        # Set up
        self._pos = pos
        self._scale = (scale, scale)
        self._disabled = disabled
        self._colors = colors
        self._matrix = matrix

        # Image
        self._rgb_array = self._colors[self._matrix]
        self._img_surface = surfarray.make_surface(self._rgb_array.swapaxes(0,1))
        self._img_surface = pygame.transform.scale(self._img_surface, multi_tuple(self._img_surface.get_size(), self._scale))

        # Rect
        self._rect =  pygame.Rect(self._pos, self._img_surface.get_size())

        # Buffer
        self._dirty = False

    # --- Public API ---
    def update(self) -> None:
        try:
            if self._disabled: return

            if self._dirty:
                self._rebuild_img()

            self._render_image()
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()


    def get_rect(self) -> pygame.Rect:
        return self._rect
    
    def set_pos(self, new_pos: Tuple[int,int]) -> None:
        self._pos = new_pos
        self._rect.topleft = new_pos

    def set_dirty(self, value: bool) -> None:
        self._dirty = value
    
    # --- Rendering ---
    def _render_image(self) -> None:
        self._surface.blit(self._img_surface, self._pos)

    def _rebuild_img(self) -> None:
        self._rgb_array = self._colors[self._matrix]
        self._img_surface = surfarray.make_surface(self._rgb_array.swapaxes(0,1))
        self._img_surface = pygame.transform.scale(self._img_surface, multi_tuple(self._img_surface.get_size(), self._scale))
        self._dirty = False
