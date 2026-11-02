from abc import ABC, abstractmethod
from typing import List, Optional
import pygame


class IInputHandler(ABC):
    """Contract for handling player input events and held-key updates."""

    @abstractmethod
    def process_event(self, event: pygame.event.Event) -> Optional[str]:
        pass

    @abstractmethod
    def update_held_inputs(self, delta_time: float) -> List[str]:
        pass