from domain.interfaces import IChallengeManager


class StandardChallengeManager(IChallengeManager):
    """Challenge manager matching the simple state checks of tetris_ver2.py
    while strictly obeying the IChallengeManager interface contract.
    """

    def __init__(self, target_score: int = 0, target_lines: int = 0, time_limit: float = 0.0) -> None:
        self.target_score: int = target_score
        self.target_lines: int = target_lines
        self.time_limit: float = time_limit
        self.elapsed_time: float = 0.0

    def update(self, delta_time: float, current_score: int, lines_cleared: int) -> None:
        self.elapsed_time += delta_time

    def check_completion(self) -> bool:
        """Original tetris_ver2.py has no completion condition."""
        return False

    def check_failure(self) -> bool:
        """Original tetris_ver2.py does not fail on a time limit."""
        return False