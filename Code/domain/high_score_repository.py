import json
from pathlib import Path
from domain.interfaces import IHighScoreRepository


class FileHighScoreRepository(IHighScoreRepository):
    """File-backed high score repository implementing IHighScoreRepository."""

    def __init__(self, file_path: str = "highscore.json") -> None:
        self.file_path: str = file_path

    def load_high_score(self) -> int:
        """Loads and returns the high score from file, defaulting to 0 if missing or corrupt."""
        path = Path(self.file_path)
        if not path.exists():
            return 0
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return int(data.get("high_score", 0))
        except (OSError, json.JSONDecodeError, ValueError):
            return 0

    def save_high_score(self, score: int) -> None:
        """Persists the high score value to JSON file."""
        try:
            path = Path(self.file_path)
            path.write_text(json.dumps({"high_score": score}), encoding="utf-8")
        except OSError:
            pass