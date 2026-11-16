import json
from pathlib import Path
from typing import Dict, List
from domain.interfaces import IHighScoreRepository


class FileHighScoreRepository(IHighScoreRepository):
    """File-backed leaderboard implementing IHighScoreRepository."""
    MAX_SCORES = 5

    def __init__(self, file_path: str = "highscore.json") -> None:
        self.file_path: str = file_path

    def load_entries(self) -> List[Dict[str, object]]:
        """Returns saved games from best to worst, or [] if the file is missing or corrupt."""
        path = Path(self.file_path)
        if not path.exists():
            return []
        try:
            saved = json.loads(path.read_text(encoding="utf-8"))["scores"]
            entries = [self._to_entry(item) for item in saved]
        except (OSError, ValueError, TypeError, KeyError):  # bad JSON is a ValueError
            return []
        entries.sort(key=lambda entry: entry["score"], reverse=True)
        return entries[:self.MAX_SCORES]

    def load_scores(self) -> List[int]:
        """Returns just the saved scores, best first."""
        return [entry["score"] for entry in self.load_entries()]

    def add_score(self, score: int, level: int = 1, difficulty: str = "normal") -> None:
        """Adds a game, keeps the best MAX_SCORES, and saves them."""
        entries = self.load_entries() + [{"score": score, "level": level, "difficulty": difficulty}]
        entries.sort(key=lambda entry: entry["score"], reverse=True)
        try:
            Path(self.file_path).write_text(json.dumps({"scores": entries[:self.MAX_SCORES]}), encoding="utf-8")
        except OSError:
            pass

    def load_high_score(self) -> int:
        """Returns the best saved score, or 0 if there are none."""
        scores = self.load_scores()
        return scores[0] if scores else 0

    def save_high_score(self, score: int) -> None:
        """Kept for the interface: puts the score on the leaderboard."""
        self.add_score(score)

    @staticmethod
    def _to_entry(item) -> Dict[str, object]:
        """Accepts a plain score (older files) or a dict with score, level, and difficulty."""
        if isinstance(item, dict):
            return {"score": int(item["score"]), "level": int(item.get("level", 1)),
                    "difficulty": str(item.get("difficulty", "normal"))}
        return {"score": int(item), "level": 1, "difficulty": "normal"}
