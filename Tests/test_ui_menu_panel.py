import pygame
import pytest

from rendering.stats_panel import PanelData, StatsPanel
from states.difficulty_state import DifficultyState
from states.game_over_state import GameOverState
from states.play_state import PlayState
from states.title_state import TitleState
from config.settings_manager import SettingsManager
from domain.interfaces import IHighScoreRepository
from domain.score_manager import GuidelineScoreManager


class FakeEngine:
    """Records the state the game switches to."""

    def __init__(self):
        self.title = "Test"
        self.settings_manager = SettingsManager()
        self.current_state = None

    def change_state(self, state):
        self.current_state = state

    def quit(self):
        pass


class FakeRepository(IHighScoreRepository):
    def load_scores(self):
        return []

    def load_entries(self):
        return []

    def add_score(self, score, level=1, difficulty="normal"):
        pass

    def load_high_score(self):
        return 0

    def save_high_score(self, score):
        pass


@pytest.fixture(autouse=True)
def pygame_fonts():
    pygame.font.init()


def key(code):
    return pygame.event.Event(pygame.KEYDOWN, key=code)


def test_start_game_opens_the_difficulty_screen():
    engine = FakeEngine()
    TitleState(engine).select_option()
    assert isinstance(engine.current_state, DifficultyState)


def test_enter_starts_normal_by_default():
    engine = FakeEngine()
    DifficultyState(engine).handle_input(key(pygame.K_RETURN))
    assert isinstance(engine.current_state, PlayState)
    assert engine.current_state.difficulty == "normal"


@pytest.mark.parametrize("code, expected", [(pygame.K_1, "easy"), (pygame.K_2, "normal"), (pygame.K_3, "hard")])
def test_number_keys_pick_a_difficulty(code, expected):
    engine = FakeEngine()
    DifficultyState(engine).handle_input(key(code))
    assert engine.current_state.difficulty == expected


def test_arrow_keys_move_the_highlight_and_wrap():
    screen = DifficultyState(FakeEngine())
    screen.handle_input(key(pygame.K_DOWN))
    assert screen.selected_difficulty == "hard"
    screen.handle_input(key(pygame.K_DOWN))
    assert screen.selected_difficulty == "easy"
    screen.handle_input(key(pygame.K_UP))
    assert screen.selected_difficulty == "hard"


def test_escape_goes_back_to_the_title():
    engine = FakeEngine()
    DifficultyState(engine).handle_input(key(pygame.K_ESCAPE))
    assert isinstance(engine.current_state, TitleState)


def test_chosen_difficulty_sets_the_fall_speed():
    engine = FakeEngine()
    DifficultyState(engine).handle_input(key(pygame.K_1))
    easy = engine.current_state.score_manager.get_fall_speed()
    DifficultyState(engine).handle_input(key(pygame.K_3))
    hard = engine.current_state.score_manager.get_fall_speed()
    assert easy > hard


def test_restart_keeps_the_difficulty():
    engine = FakeEngine()
    game_over = GameOverState(engine)
    game_over.difficulty = "hard"
    game_over.restart_game()
    assert engine.current_state.difficulty == "hard"


def test_combo_counts_clears_in_a_row_after_the_first():
    manager = GuidelineScoreManager(FakeRepository())
    assert manager.get_combo() == 0
    manager.process_line_clear(1)
    assert manager.get_combo() == 0
    manager.process_line_clear(1)
    assert manager.get_combo() == 1
    manager.process_line_clear(0)
    assert manager.get_combo() == 0


def test_stats_panel_draws_without_errors():
    surface = pygame.Surface((800, 600))
    surface.fill((255, 255, 255))
    data = PanelData(score=1200, high_score=3000, level=2, lines=12, difficulty="hard",
                     line_clears={1: 3, 2: 1, 3: 0, 4: 2}, combo=2)
    StatsPanel().render(surface, data)
    # something other than the white background was drawn in the panel area
    area = surface.subsurface((324, 200, 300, 340))
    assert any(area.get_at((x, y))[:3] != (255, 255, 255) for x in range(0, 300, 3) for y in range(0, 340, 3))


def test_game_over_lists_difficulty_and_level_when_known():
    screen = GameOverState(FakeEngine())
    screen.leaderboard_entries = [{"score": 3158, "level": 2, "difficulty": "hard"}]
    assert screen.leaderboard_lines() == ["3158   Hard   Level 2"]


def test_game_over_falls_back_to_plain_scores():
    screen = GameOverState(FakeEngine())
    screen.leaderboard = [900, 400]
    assert screen.leaderboard_lines() == ["900", "400"]
