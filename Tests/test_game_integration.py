import pygame
import pytest

from config.settings_manager import SettingsManager
from core.game_engine import GameEngine
from domain.high_score_repository import FileHighScoreRepository
from domain.piece import Piece
from domain.score_manager import GuidelineScoreManager
from states.difficulty_state import DifficultyState
from states.game_over_state import GameOverState
from states.pause_state import PauseState
from states.play_state import PlayState
from states.title_state import TitleState


@pytest.fixture
def game_engine(tmp_path, monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")

    pygame.init()
    engine = GameEngine(width=640, height=480)
    engine.settings_manager = SettingsManager(str(tmp_path / "settings.json"))
    engine.initialize()
    yield engine
    pygame.quit()


def send_key(engine, key):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))
    engine.handle_events()


def test_gameplay_flow_clears_line_and_persists_score(game_engine, tmp_path):
    engine = game_engine
    assert isinstance(engine.current_state, TitleState)

    send_key(engine, pygame.K_RETURN)
    assert isinstance(engine.current_state, DifficultyState)

    send_key(engine, pygame.K_3)
    play_state = engine.current_state
    assert isinstance(play_state, PlayState)
    assert play_state.difficulty == "hard"

    score_file = tmp_path / "scores.json"
    play_state.score_manager = GuidelineScoreManager(
        FileHighScoreRepository(str(score_file)),
        difficulty=play_state.difficulty,
    )
    play_state.saved_high_score = 0

    send_key(engine, pygame.K_ESCAPE)
    assert isinstance(engine.current_state, PauseState)
    assert engine.current_state.suspended_play_state is play_state

    send_key(engine, pygame.K_RETURN)
    assert engine.current_state is play_state

    # Complete the bottom row with an O piece, then make the next T spawn collide.
    play_state.board.grid[0][4] = (1, 1, 1)
    for column in range(play_state.board.width):
        if column not in (3, 4):
            play_state.board.grid[play_state.board.height - 1][column] = (1, 1, 1)
    play_state.active_piece = Piece("O", x=3, y=0)
    play_state.next_piece = Piece("T", x=3, y=0)

    send_key(engine, pygame.K_SPACE)

    assert isinstance(engine.current_state, GameOverState)
    assert engine.current_state.final_score == 136
    assert engine.current_state.lines_cleared == 1
    assert engine.current_state.is_high_score is True
    assert FileHighScoreRepository(str(score_file)).load_entries() == [
        {"score": 136, "level": 1, "difficulty": "hard"}
    ]

    send_key(engine, pygame.K_q)
    assert isinstance(engine.current_state, TitleState)
