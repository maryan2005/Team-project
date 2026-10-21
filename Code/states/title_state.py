from typing import TYPE_CHECKING, List, Tuple
import pygame
from states.base_state import GameState

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class TitleState(GameState):
    """Concrete implementation of GameState representing the main title menu.
    Handles user menu navigation and initiates transitions to play or settings states.
    """

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__(engine)

        # Menu options list and navigation tracking
        self.options: List[str] = ["Start Game", "Settings", "Quit"]
        self.selected_index: int = 0
        self.selected_option: str = self.options[self.selected_index]

        # UI Color definitions (RGB)
        self.TITLE_COLOR: Tuple[int, int, int] = (255, 215, 0)       # Gold
        self.SELECTED_COLOR: Tuple[int, int, int] = (0, 255, 255)    # Cyan
        self.UNSELECTED_COLOR: Tuple[int, int, int] = (180, 180, 180) # Light Gray

        # Typography setup (uses default system font if custom font asset is missing)
        self.title_font: pygame.font.Font = pygame.font.SysFont("Arial", 56, bold=True)
        self.menu_font: pygame.font.Font = pygame.font.SysFont("Arial", 32)

    def navigate_menu(self, direction: str) -> None:
        """Cycles menu option selection based on direction ('up' or 'down')
        and updates selected_option.
        """
        if direction == "up":
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif direction == "down":
            self.selected_index = (self.selected_index + 1) % len(self.options)

        self.selected_option = self.options[self.selected_index]

    def handle_input(self, event: pygame.event.Event) -> None:
        """Processes keyboard events and delegates to menu navigation or selection."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.navigate_menu("up")

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.navigate_menu("down")

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.select_option()

    def select_option(self) -> None:
        """Triggers the action associated with the currently highlighted menu option."""
        if self.selected_option == "Start Game":
            # Deferred import to prevent circular state dependencies
            from states.play_state import PlayState
            self.engine.change_state(PlayState(self.engine))

        elif self.selected_option == "Settings":
            # Deferred import to prevent circular state dependencies
            from states.settings_state import SettingsState
            self.engine.change_state(SettingsState(self.engine))

        elif self.selected_option == "Quit":
            self.engine.quit()

    def update(self, delta_time: float) -> None:
        """Updates menu animations or idle state timers if needed."""
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Renders the title banner and navigable menu items onto the screen."""
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # 1. Render Main Title
        title_surface = self.title_font.render(self.engine.title, True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        surface.blit(title_surface, title_rect)

        # 2. Render Menu Options
        start_y = screen_height // 2
        line_spacing = 50

        for index, option_text in enumerate(self.options):
            # Apply highlighted color if selected
            is_selected = (option_text == self.selected_option)
            color = self.SELECTED_COLOR if is_selected else self.UNSELECTED_COLOR
            
            # Format text with prefix indicator when selected
            display_text = f"> {option_text} <" if is_selected else option_text

            option_surface = self.menu_font.render(display_text, True, color)
            option_rect = option_surface.get_rect(center=(screen_width // 2, start_y + (index * line_spacing)))
            surface.blit(option_surface, option_rect)