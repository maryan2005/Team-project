from typing import List, TYPE_CHECKING
import pygame
from states.base_state import GameState

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class GameOverState(GameState):
    """Shows the final score, a high score message, and the top 5 leaderboard."""

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__(engine)
        self.final_score: int = 0
        self.lines_cleared: int = 0
        self.is_high_score: bool = False
        self.leaderboard: List[int] = []

        self.title_font = pygame.font.SysFont("Calibri", 65, bold=True)
        self.font = pygame.font.SysFont("Calibri", 32, bold=True)

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
        """Draws the game over screen: title, score, high score message, top 5, controls."""
        surface.fill((255, 255, 255))
        center_x = surface.get_width() // 2

        self.draw_text(surface, "Game Over", self.title_font, (255, 125, 0), center_x, 80)
        self.draw_text(surface, f"Score: {self.final_score}   Lines: {self.lines_cleared}",
                       self.font, (0, 0, 0), center_x, 160)
        if self.is_high_score:
            self.draw_text(surface, "New High Score!", self.font, (255, 165, 0), center_x, 205)

        self.draw_text(surface, "Top 5", self.font, (0, 0, 0), center_x, 270)
        for rank, score in enumerate(self.leaderboard, start=1):
            self.draw_text(surface, f"{rank}. {score}", self.font, (80, 80, 80), center_x, 270 + rank * 40)

        self.draw_text(surface, "R: restart    Q: title", self.font, (0, 0, 0), center_x, 540)

    def draw_text(self, surface: pygame.Surface, text: str, font: pygame.font.Font,
                  color: tuple, center_x: int, y: int) -> None:
        """Draws text centered horizontally at height y."""
        image = font.render(text, True, color)
        surface.blit(image, image.get_rect(center=(center_x, y)))

    def restart_game(self) -> None:
        """Starts a new gameplay session."""
        from states.play_state import PlayState
        self.engine.change_state(PlayState(self.engine))

    def return_to_title(self) -> None:
        """Returns to TitleState."""
        from states.title_state import TitleState
        self.engine.change_state(TitleState(self.engine))
