from typing import Dict
from domain.interfaces import IScoreManager, IHighScoreRepository


class GuidelineScoreManager(IScoreManager):
    """Tracks score from line clears and drops, following the IScoreManager interface."""
    LINE_CLEAR_POINTS = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
    SOFT_DROP_POINTS = 1  # per 1 cell
    HARD_DROP_POINTS = 2  # per 1 cell
    LINES_PER_LEVEL = 10
    START_FALL_SPEED = 0.5  # seconds per row at level 1
    FALL_SPEED_STEP = 0.04  # seconds removed per level
    MIN_FALL_SPEED = 0.1  # fastest allowed
    COMBO_BONUS = 50  # per earlier clear in the streak
    DIFFICULTY_SPEED = {"easy": 1.25, "normal": 1.0, "hard": 0.75}  # multiplies seconds per row

    def __init__(self, high_score_repo: IHighScoreRepository, difficulty: str = "normal") -> None:
        self.high_score_repo: IHighScoreRepository = high_score_repo
        self.difficulty: str = difficulty
        self.score: int = 0
        self.total_lines: int = 0
        self.combo: int = 0  # clears in a row before the current piece
        self.line_clear_counts: Dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}

    def process_line_clear(self, lines_cleared: int, is_t_spin: bool = False) -> int:
        """Calculates points from the clear table plus the combo bonus."""
        points = self.LINE_CLEAR_POINTS[lines_cleared]
        if lines_cleared > 0:
            points += self.COMBO_BONUS * self.combo  # first clear in a streak adds 0
            self.combo += 1
            self.line_clear_counts[lines_cleared] += 1
        else:
            self.combo = 0  # a piece locked without clearing, so the streak ends
        self.score += points
        self.total_lines += lines_cleared
        return points

    def add_drop_score(self, distance: int, is_hard_drop: bool) -> None:
        """Adds points for each cell the piece was dropped."""
        per_cell = self.HARD_DROP_POINTS if is_hard_drop else self.SOFT_DROP_POINTS
        self.score += distance * per_cell

    def get_fall_speed(self) -> float:
        """Seconds per row, faster each level and on harder difficulties, down to MIN_FALL_SPEED."""
        speed = self.START_FALL_SPEED - (self.get_level() - 1) * self.FALL_SPEED_STEP
        speed *= self.DIFFICULTY_SPEED[self.difficulty]
        return max(speed, self.MIN_FALL_SPEED)

    def get_score(self) -> int:
        return self.score

    def get_lines(self) -> int:
        """Returns the total lines cleared."""
        return self.total_lines

    def get_stats(self) -> Dict[int, int]:
        """Returns how many singles, doubles, triples, and tetrises were cleared."""
        return dict(self.line_clear_counts)

    def get_level(self) -> int:
        """Returns the current game level."""
        return 1 + self.total_lines // self.LINES_PER_LEVEL

    def reset(self) -> None:
        self.score = 0
        self.total_lines = 0
        self.combo = 0
        self.line_clear_counts = {1: 0, 2: 0, 3: 0, 4: 0}
