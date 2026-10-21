from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class GameState(ABC):
    """Abstract Base Class representing a single operational state of the game loop.
    Enforces a uniform contract for handling input, updating logic, and rendering.
    """

    def __init__(self, engine: "GameEngine") -> None:
        """Stores a reference to the central GameEngine controller to enable
        state transitions and access shared settings.
        """
        self.engine: "GameEngine" = engine

    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> None:
        """Processes individual Pygame hardware/OS events.

        Args:
            event (pygame.event.Event): The event polled from pygame.event.get().
        """
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Updates internal state logic, timers, and animations based on elapsed time.

        Args:
            delta_time (float): Time passed since last frame in seconds.
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Renders state visuals directly onto the primary display canvas.

        Args:
            surface (pygame.Surface): The active window surface from GameEngine.
        """
        pass