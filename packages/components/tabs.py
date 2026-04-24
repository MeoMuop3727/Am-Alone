import pygame
from typing import Tuple, Optional, Callable
from packages.utils.utils_math import minus_tuple, plus_tuple, multi_tuple
from .button import ButtonText
from .input import Input

class Tabs:

    """
        Initialize a Tabs UI component.

        This component renders a vertical tab panel and a corresponding content area.
        Each tab is associated with a callable that is executed every frame when the tab is active.

        Parameters
        ----------
        surface : pygame.Surface
            The target surface where the Tabs component will be rendered.

        active_index : int, optional
            The index of the initially active tab. Default is 0.

        font : Optional[pygame.font.Font], optional
            Font used to render tab labels and title. If None, a default font should be used.

        size : Tuple[int, int], optional
            Width and height of the entire Tabs component. Default is (600, 200).

        pos : Tuple[int, int], optional
            Top-left position of the Tabs component on the surface. Default is (0, 0).

        title : Optional[str], optional
            Optional title displayed above or within the Tabs component.

        title_color : Tuple[int, int, int] | str, optional
            Color of the title text. Supports RGB tuple or hex string.

        tabs_panel : Optional[list[str]], optional
            List of tab labels displayed in the tab panel.

        tabs_content : Optional[list[Callable[[], None]]], optional
            List of callables corresponding to each tab. Each callable is executed
            every frame when its tab is active.

        padding : int, optional
            Inner spacing between the component boundary and its content.

        disabled : bool, optional
            If True, disables all interactions with the Tabs component.

        background_color : Tuple[int, int, int] | str, optional
            Background color of the main content area.

        bg_panel_color : Tuple[int, int, int] | str, optional
            Default background color of tab buttons.

        bg_panel_color_active : Tuple[int, int, int] | str, optional
            Background color of the active tab.

        bg_panel_color_hover : Tuple[int, int, int] | str, optional
            Background color of a tab when hovered.

        text_color : Tuple[int, int, int] | str, optional
            Default text color of tab labels.

        text_color_hover : Tuple[int, int, int] | str, optional
            Text color when a tab is hovered.

        text_color_active : Tuple[int, int, int] | str, optional
            Text color of the active tab.

        border_width : int, optional
            Width of the border around the component.

        border_radius : int, optional
            Radius for rounded corners of the component border.

        border_color : Tuple[int, int, int] | str, optional
            Color of the component border.

        percent_width_tabs_panel : float, optional
            Proportion of total width allocated to the tab panel (range: 0.0 - 1.0).
            The remaining width is used for the content area.
    """

    def __init__(self,
                 surface: pygame.Surface,
                 active_index: int = 0,
                 font: Optional[pygame.font.Font] = None,
                 size: Tuple[int,int] = (600, 200),
                 pos: Tuple[int,int] = (0,0),
                 title: Optional[str] = None,
                 title_color: Tuple[int,int,int] | str = "#333333",
                 tabs_panel: Optional[list[str]] = None,
                 tabs_content: Optional[list[Callable[[], None]]] = None,
                 padding: int = 0,
                 disabled: bool = False,
                 background_color: Tuple[int, int, int] | str = "#F0F0F0",
                 bg_panel_color: Tuple[int,int,int] | str = "#F0F0F0",
                 bg_panel_color_active: Tuple[int, int, int] = "#333333",
                 bg_panel_color_hover: Tuple[int, int, int] = "#333333",
                 text_color: Tuple[int, int, int] | str = "#333333",
                 text_color_hover: Tuple[int,int,int] | str = "#F0F0F0",
                 text_color_active: Tuple[int,int,int] | str = "#F0F0F0",
                 border_width: int = 0,
                 border_radius: int = 0,
                 border_color: Tuple[int,int,int] | str = "#000000",
                 percent_width_tabs_panel: float = 0.35) -> None:
        # ===== Core =====
        self._surface = surface

        self._size = size
        self._pos = pos
        self._padding = (padding, padding)
        self._disabled = disabled

        # ===== Title =====
        self._title = title
        self._title_color = title_color
        self._font = font if font is not None else pygame.font.SysFont(None, 20)

        # ===== Tabs =====
        self._tabs_panel = tabs_panel if tabs_panel is not None else []
        self._tabs_contents = tabs_content if tabs_content is not None else []
        self._active_index = active_index
        self._percent_width_tabs_panel = percent_width_tabs_panel

        # ===== Colors - Background =====
        self._background_color = background_color

        self._bg_panel_color = bg_panel_color
        self._bg_panel_color_active = bg_panel_color_active
        self._bg_panel_color_hover = bg_panel_color_hover

        # ===== Colors - Text =====
        self._text_color = text_color
        self._text_color_hover = text_color_hover
        self._text_color_active = text_color_active

        # ===== Border =====
        self._border_width = (border_width, border_width)
        self._border_radius = border_radius
        self._border_color = border_color

        # ===== Frame main =====
        self._rect = pygame.Rect(self._pos, self._size)

        # ===== Others =====
        self._list_buttons: list[ButtonText] = self._set_buttons()
        self._list_contents: list[Callable] = []
        # self._obj_active_in_tab_panel = None

    
    # --- Public API ---
    # @property
    # def obj_active_in_tab_panel(self) -> any:
    #     return self._obj_active_in_tab_panel
    
    def get_pos_frame_content(self) -> Tuple[int,int]:
        x = self._pos[0] + self._size[0] * self._percent_width_tabs_panel
        y = self._pos[1]
        return plus_tuple((x,y), self._padding)
    
    def get_size_frame_content(self) -> Tuple[int,int]:
        width = self._size[0] * (1 - self._percent_width_tabs_panel)
        height = self._size[1]
        return minus_tuple((width, height), plus_tuple(self._padding, (2,2)))

    def update(self) -> None:
        try:
            if not self._disabled:
                self._draw_border()
                self._draw_frame_main()
                self._draw_frame_content()
                self._draw_tabs_panel()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def create_content(self, content: Callable | list[Callable]) -> None:
        if isinstance(content, Callable):
            self._list_contents.append(content)
        else:
            self._list_contents = content

    # --- Rendering ---
    def _draw_frame_main(self) -> None:
        frame_main = self._rect
        pygame.draw.rect(self._surface, self._background_color, frame_main, border_radius=self._border_radius)

    def _draw_border(self) -> None:
        border = pygame.Rect(
            minus_tuple(self._pos, self._border_width),
            plus_tuple(self._size, multi_tuple(self._border_width, (2,2)))
        )
        pygame.draw.rect(self._surface, self._border_color, border, border_radius=self._border_radius)

    def _draw_frame_content(self) -> any:
        if self._list_contents and self._active_index < len(self._list_contents) and self._list_contents[self._active_index]:
            self._list_contents[self._active_index]()
            # self._obj_active_in_tab_panel = self._list_contents[self._active_index]()

    def _draw_tabs_panel(self) -> None:
        for button in self._list_buttons:
            button.update()

    # --- Set up ---
    def _set_buttons(self) -> list[ButtonText]:
        list_buttons = []

        WIDTH_BUTTON = self._size[0] * self._percent_width_tabs_panel
        HEIGHT_BUTTON = self._size[1] // len(self._tabs_panel)

        for i, label in enumerate(self._tabs_panel):
            x = self._pos[0]
            y = self._pos[1] + HEIGHT_BUTTON * i 

            tab_panel = ButtonText(
                surface=self._surface,
                pos=(x,y),
                content=label,
                size=(WIDTH_BUTTON, HEIGHT_BUTTON),
                text_color=self._text_color_active if self._active_index == i else self._text_color,
                text_color_hover=self._text_color_hover,
                text_color_pressed=self._text_color_active,
                color_normal=self._bg_panel_color_active if self._active_index == i else self._bg_panel_color,
                color_hover=self._bg_panel_color_hover,
                color_pressed=self._bg_panel_color_active,
                font=self._font,
                on_click=lambda index=i: self._set_on_click(index)
            )

            list_buttons.append(tab_panel)
        
        return list_buttons

    def _set_on_click(self, i: int) -> None:
        if i < 0 or i >= len(self._tabs_panel): return

        if i == self._active_index: return

        self._active_index = i
        self._list_buttons = self._set_buttons()

        if self._tabs_contents and i < len(self._tabs_contents) and self._tabs_contents[i]:
            self._tabs_contents[i]()
