from dataclasses import dataclass
from typing import Dict
import pygame


@dataclass
class PanelData:
    """Numbers shown in the side panel."""
    score: int
    high_score: int
    level: int
    lines: int
    difficulty: str
    line_clears: Dict[int, int]  # lines cleared at once (1 to 4) -> how many times
    combo: int
    back_to_back: bool = False


class StatsPanel:
    """Draws the score, level, line statistics, and combo beside the playfield."""

    LABEL_COLOR = (90, 98, 112)
    VALUE_COLOR = (22, 26, 35)
    LEVEL_COLOR = (0, 125, 150)
    DIFFICULTY_COLOR = (200, 100, 0)
    COMBO_COLOR = (20, 140, 60)
    BACK_TO_BACK_COLOR = (200, 100, 0)
    CLEAR_NAMES = {1: "Single", 2: "Double", 3: "Triple", 4: "Tetris"}

    def __init__(self, x: int = 324, y: int = 200) -> None:
        self.x: int = x
        self.y: int = y
        self.label_font = pygame.font.SysFont("Calibri", 18)
        self.value_font = pygame.font.SysFont("Calibri", 30, bold=True)
        self.small_font = pygame.font.SysFont("Calibri", 20)

    def render(self, surface: pygame.Surface, data: PanelData) -> None:
        self._pair(surface, "Score", str(data.score), self.x, self.y, self.VALUE_COLOR)
        self._pair(surface, "High Score", str(data.high_score), self.x, self.y + 62, self.VALUE_COLOR)
        self._pair(surface, "Level", str(data.level), self.x, self.y + 124, self.LEVEL_COLOR)
        self._pair(surface, "Lines", str(data.lines), self.x + 150, self.y + 124, self.LEVEL_COLOR)
        self._pair(surface, "Difficulty", data.difficulty.capitalize(), self.x, self.y + 186, self.DIFFICULTY_COLOR)

        surface.blit(self.label_font.render("Line Stats", True, self.LABEL_COLOR), (self.x, self.y + 244))
        for index, size in enumerate((1, 2, 3, 4)):
            column, row = index % 2, index // 2
            text = f"{self.CLEAR_NAMES[size]}: {data.line_clears.get(size, 0)}"
            surface.blit(self.small_font.render(text, True, self.VALUE_COLOR),
                         (self.x + column * 150, self.y + 270 + row * 24))

        if data.combo > 0:
            surface.blit(self.small_font.render(f"Combo: {data.combo}", True, self.COMBO_COLOR),
                         (self.x, self.y + 328))
        if data.back_to_back:
            surface.blit(self.small_font.render("Back-to-Back!", True, self.BACK_TO_BACK_COLOR),
                         (self.x + 150, self.y + 328))

    def _pair(self, surface: pygame.Surface, label: str, value: str, x: int, y: int, color) -> None:
        surface.blit(self.label_font.render(label, True, self.LABEL_COLOR), (x, y))
        surface.blit(self.value_font.render(value, True, color), (x, y + 20))
