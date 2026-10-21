from typing import List, TYPE_CHECKING
import pygame
from states.base_state import GameState

if TYPE_CHECKING:
    from core.game_engine import GameEngine
    from states.play_state import PlayState


class PauseState(GameState):
    """Handles game pause state by freezing gameplay rendering and allowing resume or title exit."""

    def __init__(self, engine: "GameEngine", suspended_play_state: "PlayState") -> None:
        super().__init__(engine)
        self.suspended_play_state: "PlayState" = suspended_play_state
        self.selected_option: int = 0
        self.options: List[str] = ["Resume", "Quit to Title"]
        self.font = pygame.font.SysFont("Calibri", 30, bold=True)

    def handle_input(self, event: pygame.event.Event) -> None:
        """Processes key presses for menu option navigation and selection."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.resume_game()
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.selected_option == 0:
                    self.resume_game()
                else:
                    self.return_to_title()

    def update(self, delta_time: float) -> None:
        """No game updates take place while paused."""
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Renders suspended board state under a translucent dark overlay and pause menu options."""
        # Draw background play state underneath
        self.suspended_play_state.draw(surface)

        # Draw translucent dark overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Render menu options
        for idx, option in enumerate(self.options):
            color = (255, 215, 0) if idx == self.selected_option else (255, 255, 255)
            text_surf = self.font.render(option, True, color)
            rect = text_surf.get_rect(center=(surface.get_width() // 2, 200 + idx * 50))
            surface.blit(text_surf, rect)

    def resume_game(self) -> None:
        """Restores the active play state."""
        self.engine.change_state(self.suspended_play_state)

    def return_to_title(self) -> None:
        """Navigates back to TitleState."""
        from states.title_state import TitleState
        self.engine.change_state(TitleState(self.engine))