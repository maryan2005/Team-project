from typing import TYPE_CHECKING
import pygame
from states.base_state import GameState

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class GameOverState(GameState):
    """Handles Game Over screen display matching original tetris_ver2 style. TO DO: Implement high score logic."""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__(engine)
        self.final_score: int = 0
        self.lines_cleared: int = 0
        self.is_high_score: bool = False
        
        self.font = pygame.font.SysFont("Calibri", 65, bold=True)

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handles restart or quit key bindings."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.restart_game()
            elif event.key in (pygame.K_q, pygame.K_ESCAPE, pygame.K_RETURN):
                self.return_to_title()

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Renders Game Over messages matching tetris_ver2 colors and positioning."""
        surface.fill((255, 255, 255))  # White background

        text_game_over = self.font.render("Game Over", True, (255, 125, 0))
        text_game_over1 = self.font.render("Enter q to Quit", True, (255, 215, 0))

        surface.blit(text_game_over, (20, 200))
        surface.blit(text_game_over1, (25, 265))

    def restart_game(self) -> None:
        """Starts a new gameplay session."""
        from states.play_state import PlayState
        self.engine.change_state(PlayState(self.engine))

    def return_to_title(self) -> None:
        """Returns to TitleState."""
        from states.title_state import TitleState
        self.engine.change_state(TitleState(self.engine))