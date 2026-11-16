from typing import TYPE_CHECKING, List
import pygame
from states.base_state import GameState

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class DifficultyState(GameState):
    """Lets the player pick Easy, Normal, or Hard before a game starts."""

    DIFFICULTIES: List[str] = ["easy", "normal", "hard"]
    CONTROLS: List[str] = [
        "Left / Right: move",
        "Up: rotate      Z: rotate back",
        "Down: soft drop      Space: hard drop",
        "C: hold      Esc: pause",
    ]

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__(engine)
        self.selected_index: int = 1  # Normal

        self.TITLE_COLOR = (255, 215, 0)
        self.SELECTED_COLOR = (0, 255, 255)
        self.UNSELECTED_COLOR = (180, 180, 180)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 32)
        self.help_font = pygame.font.SysFont("Arial", 22)

    @property
    def selected_difficulty(self) -> str:
        return self.DIFFICULTIES[self.selected_index]

    def move_selection(self, step: int) -> None:
        """Moves the highlight up (-1) or down (+1), wrapping around."""
        self.selected_index = (self.selected_index + step) % len(self.DIFFICULTIES)

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_UP, pygame.K_w):
            self.move_selection(-1)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.move_selection(1)
        elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
            self.selected_index = event.key - pygame.K_1
            self.start_game()
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.start_game()
        elif event.key == pygame.K_ESCAPE:
            self.go_back()

    def start_game(self) -> None:
        """Starts a game at the highlighted difficulty."""
        from states.play_state import PlayState
        self.engine.change_state(PlayState(self.engine, difficulty=self.selected_difficulty))

    def go_back(self) -> None:
        """Returns to the title menu."""
        from states.title_state import TitleState
        self.engine.change_state(TitleState(self.engine))

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        width = surface.get_width()
        title = self.title_font.render("Choose Difficulty", True, self.TITLE_COLOR)
        surface.blit(title, title.get_rect(center=(width // 2, 90)))

        for index, name in enumerate(self.DIFFICULTIES):
            selected = index == self.selected_index
            label = f"{index + 1} - {name.capitalize()}"
            text = f"> {label} <" if selected else label
            color = self.SELECTED_COLOR if selected else self.UNSELECTED_COLOR
            image = self.menu_font.render(text, True, color)
            surface.blit(image, image.get_rect(center=(width // 2, 190 + index * 50)))

        hint = self.help_font.render("Press 1, 2, or 3, or choose and press Enter", True, self.UNSELECTED_COLOR)
        surface.blit(hint, hint.get_rect(center=(width // 2, 360)))

        for index, line in enumerate(self.CONTROLS):
            image = self.help_font.render(line, True, self.UNSELECTED_COLOR)
            surface.blit(image, image.get_rect(center=(width // 2, 430 + index * 32)))
