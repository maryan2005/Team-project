import pytest
from domain.high_score_repository import FileHighScoreRepository
from domain.score_manager import GuidelineScoreManager


@pytest.fixture
def manager():
    # A fresh score manager for every test
    return GuidelineScoreManager(FileHighScoreRepository())


@pytest.mark.parametrize("lines, points", [(0, 0), (1, 100), (2, 300), (3, 500), (4, 800)])
def test_line_clear_points(manager, lines, points):
    assert manager.process_line_clear(lines) == points
    assert manager.get_score() == points


def test_scores_add_up(manager):
    manager.process_line_clear(1)
    manager.process_line_clear(0)  # a lock with no clear, so no combo
    manager.process_line_clear(4)
    assert manager.get_score() == 900


def test_hard_drop_scores_two_per_cell(manager):
    manager.add_drop_score(10, is_hard_drop=True)
    assert manager.get_score() == 20


def test_soft_drop_scores_one_per_cell(manager):
    manager.add_drop_score(10, is_hard_drop=False)
    assert manager.get_score() == 10


def test_lines_are_counted(manager):
    manager.process_line_clear(2)
    manager.process_line_clear(3)
    assert manager.get_lines() == 5


def test_level_goes_up_every_ten_lines(manager):
    assert manager.get_level() == 1
    manager.total_lines = 9
    assert manager.get_level() == 1
    manager.total_lines = 10
    assert manager.get_level() == 2


@pytest.mark.parametrize("level, speed", [(1, 0.5), (10, 0.14), (11, 0.1), (50, 0.1)])
def test_fall_speed_by_level(manager, level, speed):
    manager.total_lines = (level - 1) * 10  # lines needed to reach that level
    assert manager.get_fall_speed() == pytest.approx(speed)


def test_reset(manager):
    manager.process_line_clear(4)
    manager.reset()
    assert manager.get_score() == 0
    assert manager.get_lines() == 0
    assert manager.get_level() == 1


def test_stats_count_each_clear_type(manager):
    manager.process_line_clear(1)
    manager.process_line_clear(1)
    manager.process_line_clear(4)
    assert manager.get_stats() == {1: 2, 2: 0, 3: 0, 4: 1}


def test_stats_ignore_zero_line_clears(manager):
    manager.process_line_clear(0)
    assert manager.get_stats() == {1: 0, 2: 0, 3: 0, 4: 0}


def test_stats_returns_a_copy(manager):
    manager.get_stats()[1] = 99  # changing the copy must not change the real counts
    assert manager.get_stats()[1] == 0


def test_reset_clears_stats(manager):
    manager.process_line_clear(2)
    manager.reset()
    assert manager.get_stats() == {1: 0, 2: 0, 3: 0, 4: 0}


def test_first_clear_has_no_combo_bonus(manager):
    assert manager.process_line_clear(1) == 100


def test_second_clear_in_a_row_gets_bonus(manager):
    manager.process_line_clear(1)
    assert manager.process_line_clear(1) == 150


def test_combo_bonus_keeps_growing(manager):
    manager.process_line_clear(1)
    manager.process_line_clear(1)
    assert manager.process_line_clear(1) == 200


def test_lock_without_clear_ends_the_combo(manager):
    manager.process_line_clear(1)
    manager.process_line_clear(0)
    assert manager.process_line_clear(1) == 100


def test_reset_clears_the_combo(manager):
    manager.process_line_clear(1)
    manager.process_line_clear(1)
    manager.reset()
    assert manager.process_line_clear(1) == 100



@pytest.mark.parametrize("difficulty, level, speed", [
    ("easy", 1, 0.625),
    ("hard", 1, 0.375),
    ("easy", 10, 0.175),
    ("hard", 10, 0.105),
    ("hard", 20, 0.1),  # hits the speed cap
])
def test_fall_speed_by_difficulty(difficulty, level, speed):
    manager = GuidelineScoreManager(FileHighScoreRepository(), difficulty=difficulty)
    manager.total_lines = (level - 1) * 10
    assert manager.get_fall_speed() == pytest.approx(speed)


def test_difficulty_defaults_to_normal(manager):
    assert manager.difficulty == "normal"
