from domain.interfaces import IScoreManager, IHighScoreRepository


class GuidelineScoreManager(IScoreManager):
    """Score manager matching the exact scoring formula (Score += lines ** 2)
    from tetris_ver2.py while strictly obeying the IScoreManager interface contract.
    """

    def __init__(self, high_score_repo: IHighScoreRepository) -> None:
        self.high_score_repo: IHighScoreRepository = high_score_repo
        self.score: int = 0
        self.level: int = 1
        self.total_lines: int = 0

    def process_line_clear(self, lines_cleared: int, is_t_spin: bool = False) -> int:
        """Calculates points using the lines ** 2 formula from tetris_ver2.py."""
        points = lines_cleared ** 2
        self.score += points
        self.total_lines += lines_cleared
        return points

    def add_drop_score(self, distance: int, is_hard_drop: bool) -> None:
        """No drop bonus scoring in tetris_ver2.py."""
        pass

    def get_fall_speed(self) -> float:
        """Fixed fall speed step matching the original loop timing."""
        return 0.5

    def get_score(self) -> int:
        return self.score

    def get_lines(self) -> int:
        """Returns the total lines cleared."""
        return self.total_lines

    def get_level(self) -> int:
        """Returns the current game level."""
        return self.level

    def reset(self) -> None:
        self.score = 0
        self.level = 1
        self.total_lines = 0