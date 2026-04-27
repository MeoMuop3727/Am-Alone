import pygame
from packages.utils.utils_math import minus_tuple, plus_tuple, multi_tuple
from typing import Optional, Tuple, Literal
from .textbox import TextBox
from .button import ButtonText

class NotifyBox:

    """
        Initialize a notification box UI component.

        Args:
            surface (pygame.Surface):
                The target surface where the notification box will be rendered.

            pos (Tuple[int, int]):
                Top-left position (x, y) of the notification box.

            size (Tuple[int, int]):
                Width and height of the notification box.

            title (Optional[str]):
                Title text displayed in the title bar. If None, no title is shown.

            content (Optional[str]):
                Main content text of the notification.

            font (Optional[pygame.font.Font]):
                Font used for rendering text. If None, a default font should be used.

            text_color (Tuple[int, int, int] | str):
                Color of the content text. Accepts RGB tuple or hex string.

            title_color (Tuple[int, int, int] | str):
                Color of the title text.

            background_color (Tuple[int, int, int] | str):
                Background color of the notification box.

            border_color (Tuple[int, int, int] | str):
                Color of the border.

            border_width (int):
                Width of the border. Set to 0 for no border.

            border_radius (int):
                Radius for rounded corners of the notification box.

            type (Literal["info", "warning", "error", "success"]):
                Type of notification. Used to determine default styling behavior.

            title_bg_color (Optional[Tuple[int, int, int] | str]):
                Background color of the title bar. If None, it may be derived from `type`.

            button_bg_color (Tuple[int, int, int] | str):
                Background color of the close button in normal state.

            button_text_color (Tuple[int, int, int] | str):
                Text color of the close button in normal state.

            button_bg_color_hover (Tuple[int, int, int] | str):
                Background color of the close button when hovered.

            button_text_color_hover (Tuple[int, int, int] | str):
                Text color of the close button when hovered.

            button_bg_color_pressed (Tuple[int, int, int] | str):
                Background color of the close button when pressed.

            button_text_color_pressed (Tuple[int, int, int] | str):
                Text color of the close button when pressed.

            disabled (bool):
                If True, the notification is inactive and does not respond to interaction.

            button_border_radius (int):
                Border radius of the close button.

            button_border_width (int):
                Border width of the close button.

            button_border_color (Tuple[int, int, int] | str):
                Border color of the close button.

            line_height (int):
                Custom line height for rendering multi-line content text.
                If 0, it defaults to the font's natural line height.

            padding (int):
                Inner spacing between the content and the box edges.
    """

    def __init__(self,
                 surface: pygame.Surface,
                 pos: Tuple[int,int] = (0,0),
                 size: Tuple[int,int] = (300,150),
                 title: Optional[str] = None,
                 content: Optional[str] = None,
                 font: Optional[pygame.font.Font] = None,
                 text_color: Tuple[int,int,int] | str = "#333333",
                 title_color: Tuple[int,int,int] | str = "#FFFFFF",
                 background_color: Tuple[int,int,int] | str = "#F0F0F0",
                 border_color: Tuple[int,int,int] | str = "#000000",
                 border_width: int = 0,
                 border_radius: int = 0, 
                 type: Literal["info", "warning", "error", "success"] = "info",
                 title_bg_color: Optional[Tuple[int,int,int] | str] = None,
                 button_bg_color: Tuple[int,int,int] | str = "#DA2E2E",
                 button_text_color: Tuple[int,int,int] | str = "#333333",
                 button_bg_color_hover: Tuple[int,int,int] | str = "#EF5959",
                 button_text_color_hover: Tuple[int,int,int] | str = "#F0F0F0",
                 button_bg_color_pressed: Tuple[int,int,int] | str = "#EF5959",
                 button_text_color_pressed: Tuple[int,int,int] | str = "#F0F0F0",
                 disabled: bool = False,
                 button_border_radius: int = 0,
                 button_border_width: int = 0,
                 button_border_color: Tuple[int,int,int] | str = "#F0F0F0",
                 line_height: int = 0,
                 padding: int = 0):
        self._surface = surface

        # Layout
        self._pos = pos
        self._size = size

        # Content
        self._title = title
        self._content = content
        self._font = font if font is not None else pygame.font.SysFont(None, 20)
        self._line_height = line_height

        # Padding
        self._padding = padding

        # Colors - text
        self._text_color = text_color
        self._title_color = title_color

        # Colors - background & border
        self._background_color = background_color
        self._border_color = border_color
        self._border_width = (border_width, border_width)
        self._border_radius = border_radius

        # Type
        self._type = type
        self._list_title_bg_color = {
            "info": "#2F80ED",
            "warning": "#F2C94C",
            "error": "#EB5757",
            "success": "#27AE60"
        }

        # Title background
        self._title_bg_color = title_bg_color if title_bg_color is not None else self._list_title_bg_color[type]

        # Button colors - normal
        self._button_bg_color = button_bg_color
        self._button_text_color = button_text_color

        # Button colors - hover
        self._button_bg_color_hover = button_bg_color_hover
        self._button_text_color_hover = button_text_color_hover

        # Button colors - pressed
        self._button_bg_color_pressed = button_bg_color_pressed
        self._button_text_color_pressed = button_text_color_pressed

        # Button state
        self._disabled = disabled

        # Button border
        self._button_border_radius = button_border_radius
        self._button_border_width = button_border_width
        self._button_border_color = button_border_color

        # Main frame
        self._rect = pygame.Rect(pos, size)

        # Others
        self._percent_height_frame_title = 0
        self._button_close = ButtonText(
            surface=self._surface,
            content="x",
            font=self._font,
            text_color=self._button_text_color,
            text_color_hover=self._button_text_color_hover,
            text_color_pressed=self._button_text_color_pressed,
            color_normal=self._button_bg_color,
            color_hover=self._button_bg_color_hover,
            color_pressed=self._button_bg_color_pressed,
            border_color=self._button_border_color,
            border_radius=self._button_border_radius,
            border_width=self._button_border_width,
            size=(self._font.get_height(), self._font.get_height()),
            pos=(
                self._pos[0] + self._size[0] - self._font.get_height() - 5,
                self._pos[1] + 5
            ),
            on_click=lambda: self._on_click_button_close()
        )

    # ===== Public API =====
    @property
    def disable(self) -> bool:
        return self._disabled
    
    @disable.setter
    def disable(self, value: bool) -> None:
        self._disabled = value
    
    def update(self) -> None:
        try:
            if not self._disabled:
                self._draw_border()
                self._draw_frame_content()
                self._draw_frame_title()
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    # ===== Rendering =====
    def _draw_border(self) -> None:
        border = pygame.Rect(
            minus_tuple(self._pos, self._border_width),
            plus_tuple(self._size, multi_tuple(self._border_width, (2,2)))
        )
        pygame.draw.rect(self._surface, self._border_color, border, border_radius=self._border_radius)
    
    def _draw_frame_content(self) -> None:
        HEIGHT_FRAME_TITLE = self._size[1] * self._percent_height_frame_title
        HEIGHT_FRAME_CONTENT = self._size[1] - HEIGHT_FRAME_TITLE

        x, y = self._pos[0], self._pos[1] + HEIGHT_FRAME_TITLE

        frame_main = pygame.Rect((x,y), (self._size[0], HEIGHT_FRAME_CONTENT))  

        text_box = TextBox(
            surface=self._surface,
            content=self._content,
            font=self._font,
            text_color=self._text_color,
            size=(self._size[0], HEIGHT_FRAME_CONTENT),
            pos=(x,y),
            line_height=self._line_height,
            padding=self._padding
        )     

        # Draw frame content
        pygame.draw.rect(self._surface, self._background_color, frame_main, border_bottom_left_radius=self._border_radius, border_bottom_right_radius=self._border_radius)

        # Draw text box
        text_box.update()

    def _draw_frame_title(self) -> None:
        PADDING = 5
        HEIGHT_FRAME_TITLE = self._font.get_height() + PADDING * 2

        self._percent_height_frame_title = HEIGHT_FRAME_TITLE / self._size[1]

        frame_title = pygame.Rect(self._pos, (self._size[0], HEIGHT_FRAME_TITLE))

        text_surface = self._font.render(self._title, True, self._title_color)
        text_rect = text_surface.get_rect(center=frame_title.center)

        # Draw frame title
        pygame.draw.rect(self._surface, self._title_bg_color, frame_title, border_top_left_radius=self._border_radius, border_top_right_radius=self._border_radius)

        # Draw title
        self._surface.blit(text_surface, text_rect)

        # Draw button close
        self._button_close.update()

    # ===== Set up =====
    def _on_click_button_close(self) -> None:
        if not self._disabled:
            self._disabled = True
