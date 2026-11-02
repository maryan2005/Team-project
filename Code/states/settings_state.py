from typing import TYPE_CHECKING
import pygame
from states.base_state import GameState

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class SettingsState(GameState):
    """Temporary stub implementation of SettingsState for testing navigation flows."""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__(engine)
        self.font = pygame.font.SysFont("Arial", 36)

    def handle_input(self, event: pygame.event.Event) -> None:
        # Press Escape or Backspace to return to Title Menu
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            from states.title_state import TitleState
            self.engine.change_state(TitleState(self.engine))

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        text_surface = self.font.render("SETTINGS STATE (Press ESC to return)", True, (0, 200, 255))
        text_rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(text_surface, text_rect)