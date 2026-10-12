import pygame

from config.settings_manager import SettingsManager
from input.input_handler import InputHandler


def make_handler(das_delay=0.15, arr_rate=0.05):
    settings = SettingsManager()
    settings.das_delay = das_delay
    settings.arr_rate = arr_rate
    return InputHandler(settings)


def key_event(event_type, key):
    return pygame.event.Event(event_type, key=key)


def test_horizontal_key_moves_immediately_and_repeats_after_das():
    handler = make_handler()

    assert handler.process_event(key_event(pygame.KEYDOWN, pygame.K_LEFT)) == "move_left"
    assert handler.update_held_inputs(0.14) == []
    assert handler.update_held_inputs(0.01) == ["move_left"]
    assert handler.update_held_inputs(0.05) == ["move_left"]


def test_arr_catches_up_for_elapsed_time_and_keyup_stops_repeat():
    handler = make_handler()
    handler.process_event(key_event(pygame.KEYDOWN, pygame.K_RIGHT))

    assert handler.update_held_inputs(0.30) == [
        "move_right",
        "move_right",
        "move_right",
        "move_right",
    ]
    handler.process_event(key_event(pygame.KEYUP, pygame.K_RIGHT))
    assert handler.update_held_inputs(1.0) == []


def test_repeated_keydown_does_not_bypass_das():
    handler = make_handler()
    assert handler.process_event(key_event(pygame.KEYDOWN, pygame.K_LEFT)) == "move_left"
    assert handler.process_event(key_event(pygame.KEYDOWN, pygame.K_LEFT)) is None
    assert handler.update_held_inputs(0.14) == []


def test_most_recent_horizontal_press_controls_repeat():
    handler = make_handler()
    handler.process_event(key_event(pygame.KEYDOWN, pygame.K_LEFT))
    handler.process_event(key_event(pygame.KEYDOWN, pygame.K_RIGHT))

    assert handler.update_held_inputs(0.15) == ["move_right"]
    handler.process_event(key_event(pygame.KEYUP, pygame.K_RIGHT))
    assert handler.update_held_inputs(0.15) == ["move_left"]


def test_releasing_inactive_direction_does_not_restart_das():
    handler = make_handler()
    handler.process_event(key_event(pygame.KEYDOWN, pygame.K_LEFT))
    handler.process_event(key_event(pygame.KEYDOWN, pygame.K_RIGHT))

    assert handler.update_held_inputs(0.10) == []
    handler.process_event(key_event(pygame.KEYUP, pygame.K_LEFT))
    assert handler.update_held_inputs(0.05) == ["move_right"]


def test_rotation_bindings_emit_clockwise_and_counterclockwise_actions():
    handler = make_handler()

    assert handler.process_event(key_event(pygame.KEYDOWN, pygame.K_UP)) == "rotate"
    assert handler.process_event(key_event(pygame.KEYDOWN, pygame.K_z)) == "rotate_ccw"


def test_rotation_bindings_can_be_reconfigured():
    handler = make_handler()
    handler.settings_manager.set_binding("rotate", pygame.K_x)
    handler.settings_manager.set_binding("rotate_ccw", pygame.K_c)

    assert handler.process_event(key_event(pygame.KEYDOWN, pygame.K_x)) == "rotate"
    assert handler.process_event(key_event(pygame.KEYDOWN, pygame.K_c)) == "rotate_ccw"
