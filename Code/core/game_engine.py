from typing import Optional
import sys
import pygame
from states.base_state import GameState
from states.title_state import TitleState
from config.settings_manager import SettingsManager


class GameEngine:
    """Central engine controller managing the game loop, screen surface,
    state transitions, and globally available configurations.
    """

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "Team Yellow",
        target_fps: int = 60,
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.target_fps: int = target_fps

        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.is_running: bool = False

        # Centralized Settings Manager instance
        self.settings_manager: SettingsManager = SettingsManager()

        # State Pattern variable
        self.current_state: Optional[GameState] = None

    def initialize(self) -> None:
        """Boots Pygame hardware, loads settings, and sets the starting state."""
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.settings_manager.load_settings()
        
        # Safely set default starting state after hardware is ready
        self.change_state(TitleState(self))
        self.is_running = True

    def change_state(self, new_state: GameState) -> None:
        """Transitions the engine to a new GameState instance."""
        self.current_state = new_state

    def handle_events(self) -> None:
        """Processes OS and hardware events, forwarding them to the active state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return

            if self.current_state:
                self.current_state.handle_input(event)

    def update(self, delta_time: float) -> None:
        """Delegates frame updates and time progression to the current state."""
        if self.current_state:
            self.current_state.update(delta_time)

    def render(self) -> None:
        """Clears the display surface and delegates rendering to the active state."""
        if self.screen is None:
            return

        # Clear screen with black background default
        self.screen.fill((0, 0, 0))

        if self.current_state:
            self.current_state.draw(self.screen)

        pygame.display.flip()

    def run(self) -> None:
        """Executes the core game loop using delta time for tick-rate stability."""
        if not self.is_running:
            self.initialize()

        while self.is_running:
            # Calculate time passed since last frame in seconds
            delta_time: float = self.clock.tick(self.target_fps) / 1000.0

            self.handle_events()
            self.update(delta_time)
            self.render()

        pygame.quit()
        sys.exit()

    def quit(self) -> None:
        """Gracefully halts the execution loop."""
        self.is_running = False