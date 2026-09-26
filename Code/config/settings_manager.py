import json
from pathlib import Path
from typing import Dict, Optional


class SettingsManager:
    """Loads, manages, and persists user settings for Team Yellow Tetris."""

    def __init__(self, file_path: Optional[str] = None) -> None:
        self._file_path: str = str(
            Path(file_path) if file_path else Path(__file__).with_name("settings.json")
        )
        self._volume: float = 0.7
        self._key_bindings: Dict[str, int] = {
            "move_left": 97,    # pygame.K_a
            "move_right": 100,  # pygame.K_d
            "soft_drop": 115,   # pygame.K_s
            "rotate": 119,      # pygame.K_w
            "hard_drop": 32,    # pygame.K_SPACE
        }
        self._das_delay: float = 0.15
        self._arr_rate: float = 0.05

    @property
    def das_delay(self) -> float:
        return self._das_delay

    @das_delay.setter
    def das_delay(self, value: float) -> None:
        self._das_delay = max(0.0, value)

    @property
    def arr_rate(self) -> float:
        return self._arr_rate

    @arr_rate.setter
    def arr_rate(self, value: float) -> None:
        self._arr_rate = max(0.0, value)

    def load_settings(self) -> None:
        """Load valid settings, keeping defaults for missing or invalid values."""
        try:
            data = json.loads(Path(self._file_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        if not isinstance(data, dict):
            return

        volume = data.get("volume")
        if isinstance(volume, (int, float)) and not isinstance(volume, bool):
            self._volume = float(max(0.0, min(1.0, volume)))

        bindings = data.get("key_bindings")
        if isinstance(bindings, dict):
            self._key_bindings.update(
                {
                    action: key
                    for action, key in bindings.items()
                    if isinstance(action, str)
                    and isinstance(key, int)
                    and not isinstance(key, bool)
                }
            )

        das_delay = data.get("das_delay")
        if (
            isinstance(das_delay, (int, float))
            and not isinstance(das_delay, bool)
            and das_delay >= 0
        ):
            self._das_delay = float(das_delay)

        arr_rate = data.get("arr_rate")
        if (
            isinstance(arr_rate, (int, float))
            and not isinstance(arr_rate, bool)
            and arr_rate >= 0
        ):
            self._arr_rate = float(arr_rate)

    def save_settings(self) -> None:
        """Persists current settings to disk in JSON format."""
        data = {
            "volume": self._volume,
            "key_bindings": self._key_bindings,
            "das_delay": self._das_delay,
            "arr_rate": self._arr_rate,
        }
        settings_path = Path(self._file_path)
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_binding(self, action: str, default: Optional[int] = None) -> Optional[int]:
        """Safely retrieves the key binding for a specified action."""
        return self._key_bindings.get(action, default)

    def set_binding(self, action: str, key: int) -> None:
        """Updates the key binding for a specified action."""
        self._key_bindings[action] = key

    def get_volume(self) -> float:
        return self._volume

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))