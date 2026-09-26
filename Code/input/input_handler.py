from typing import Dict, List, Optional
import pygame
from config.settings_manager import SettingsManager
from input.interfaces import IInputHandler


class InputHandler(IInputHandler):
    """Translates Pygame events into game actions matching tetris_ver2 key bindings."""

    def __init__(self, settings_manager: SettingsManager) -> None:
        self.settings_manager: SettingsManager = settings_manager
        self.das_timer: float = 0.0
        self.arr_timer: float = 0.0
        self.held_keys: Dict[int, bool] = {}

    def process_event(self, event: pygame.event.Event) -> Optional[str]:
        """Maps single key presses directly to action strings. TO DO: DYNAMIC INPUT HANDLING AND SOFT DROP"""
        if event.type == pygame.KEYDOWN:
            self.held_keys[event.key] = True

            if event.key == pygame.K_UP:
                return "rotate"
            elif event.key == pygame.K_LEFT:
                return "move_left"
            elif event.key == pygame.K_RIGHT:
                return "move_right"
            elif event.key == pygame.K_SPACE:
                return "hard_drop"
            elif event.key == pygame.K_DOWN:
                return "soft_drop"

        elif event.type == pygame.KEYUP:
            self.held_keys[event.key] = False

        return None

    def update_held_inputs(self, delta_time: float) -> List[str]:
        """Unused for tetris_ver2 basic discrete movement logic."""
        return []