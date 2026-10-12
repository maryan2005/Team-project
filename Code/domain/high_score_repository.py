import json
from pathlib import Path
from typing import List
from domain.interfaces import IHighScoreRepository


class FileHighScoreRepository(IHighScoreRepository):
    """File-backed leaderboard implementing IHighScoreRepository."""
    MAX_SCORES = 5

    def __init__(self, file_path: str = "highscore.json") -> None:
        self.file_path: str = file_path

    def load_scores(self) -> List[int]:
        """Returns saved scores from best to worst, or [] if the file is missing or corrupt."""
        path = Path(self.file_path)
        if not path.exists():
            return []
        try:
            saved = json.loads(path.read_text(encoding="utf-8"))["scores"]
            return sorted((int(score) for score in saved), reverse=True)[:self.MAX_SCORES]
        except (OSError, ValueError, TypeError, KeyError):  # bad JSON is a ValueError
            return []

    def add_score(self, score: int) -> None:
        """Adds a score, keeps the best MAX_SCORES, and saves them."""
        scores = sorted(self.load_scores() + [score], reverse=True)[:self.MAX_SCORES]
        try:
            Path(self.file_path).write_text(json.dumps({"scores": scores}), encoding="utf-8")
        except OSError:
            pass

    def load_high_score(self) -> int:
        """Returns the best saved score, or 0 if there are none."""
        scores = self.load_scores()
        return scores[0] if scores else 0

    def save_high_score(self, score: int) -> None:
        """Kept for the interface: puts the score on the leaderboard."""
        self.add_score(score)
