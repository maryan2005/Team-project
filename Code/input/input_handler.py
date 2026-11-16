from typing import Dict, List, Optional
import pygame
from config.settings_manager import SettingsManager
from input.interfaces import IInputHandler


class InputHandler(IInputHandler):
    """Translates Pygame events into game actions with DAS/ARR movement repeat."""

    def __init__(self, settings_manager: SettingsManager) -> None:
        self.settings_manager: SettingsManager = settings_manager
        self.das_timer: float = 0.0
        self.arr_timer: float = 0.0
        self.held_keys: Dict[int, bool] = {}

    def process_event(self, event: pygame.event.Event) -> Optional[str]:
        """Maps key presses to actions and starts horizontal repeat tracking."""
        if event.type == pygame.KEYDOWN:
            was_held = self.held_keys.get(event.key, False)
            self.held_keys[event.key] = True

            if event.key == self.settings_manager.get_binding("rotate", pygame.K_UP):
                return "rotate"
            elif event.key == self.settings_manager.get_binding("rotate_ccw", pygame.K_z):
                return "rotate_ccw"
            elif event.key == pygame.K_LEFT:
                if was_held:
                    return None
                self.das_timer = 0.0
                self.arr_timer = 0.0
                return "move_left"
            elif event.key == pygame.K_RIGHT:
                if was_held:
                    return None
                self.das_timer = 0.0
                self.arr_timer = 0.0
                return "move_right"
            elif event.key == pygame.K_SPACE:
                return "hard_drop"
            elif event.key == self.settings_manager.get_binding("hold", pygame.K_c):
                return "hold_piece"
            elif event.key == pygame.K_DOWN:
                return "soft_drop"

        elif event.type == pygame.KEYUP:
            active_horizontal_key = next(
                (
                    key
                    for key in reversed(self.held_keys)
                    if key in (pygame.K_LEFT, pygame.K_RIGHT)
                ),
                None,
            )
            self.held_keys.pop(event.key, None)
            if event.key == active_horizontal_key:
                self.das_timer = 0.0
                self.arr_timer = 0.0

        return None

    def update_held_inputs(self, delta_time: float) -> List[str]:
        """Repeats the most recently pressed horizontal direction after DAS."""
        direction = next(
            (
                "move_left" if key == pygame.K_LEFT else "move_right"
                for key in reversed(self.held_keys)
                if key in (pygame.K_LEFT, pygame.K_RIGHT)
            ),
            None,
        )
        if direction is None:
            self.das_timer = 0.0
            self.arr_timer = 0.0
            return []

        das_delay = self.settings_manager.das_delay
        arr_rate = self.settings_manager.arr_rate
        previous_das = self.das_timer
        self.das_timer += max(0.0, delta_time)

        actions: List[str] = []
        if previous_das < das_delay:
            if self.das_timer < das_delay:
                return actions
            self.arr_timer += self.das_timer - das_delay
            actions.append(direction)
        else:
            self.arr_timer += max(0.0, delta_time)
            if arr_rate <= 0.0:
                return [direction]

        if arr_rate <= 0.0:
            self.arr_timer = 0.0
            return actions

        repeat_count = int((self.arr_timer + 1e-9) / arr_rate)
        if repeat_count:
            self.arr_timer = max(0.0, self.arr_timer - repeat_count * arr_rate)
            actions.extend([direction] * repeat_count)
        return actions