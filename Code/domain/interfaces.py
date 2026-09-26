from abc import ABC, abstractmethod


class IScoreManager(ABC):
    """Contract for score tracking, combos, and gravity fall rates."""

    @abstractmethod
    def process_line_clear(self, lines_cleared: int, is_t_spin: bool = False) -> int:
        pass

    @abstractmethod
    def add_drop_score(self, distance: int, is_hard_drop: bool) -> None:
        pass

    @abstractmethod
    def get_fall_speed(self) -> float:
        pass

    @abstractmethod
    def get_score(self) -> int:
        pass

    @abstractmethod
    def get_lines(self) -> int:
        pass

    @abstractmethod
    def get_level(self) -> int:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass


class IChallengeManager(ABC):
    """Contract for optional game mode conditions or challenge modifiers."""

    @abstractmethod
    def update(self, delta_time: float, current_score: int, lines_cleared: int) -> None:
        pass

    @abstractmethod
    def check_completion(self) -> bool:
        pass

    @abstractmethod
    def check_failure(self) -> bool:
        pass


class IHighScoreRepository(ABC):
    """Contract for loading and persisting high scores."""

    @abstractmethod
    def load_high_score(self) -> int:
        pass

    @abstractmethod
    def save_high_score(self, score: int) -> None:
        pass