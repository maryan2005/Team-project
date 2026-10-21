import random
from typing import List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.piece import Piece, TETROMINO_SHAPES


class Board:
    """Manages the grid state, piece collision checks, piece locking,
    and row clearing operations according to the UML specification.
    """

    def __init__(self, width: int = 10, height: int = 20) -> None:
        self.width: int = width
        self.height: int = height
        # Matrix storing None for empty cells or (R, G, B) color tuple for locked blocks
        self.grid: List[List[Optional[Tuple[int, int, int]]]] = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]

    def is_valid_position(self, piece: "Piece", offset_x: int = 0, offset_y: int = 0) -> bool:
        """Checks whether placing or moving the piece with an offset is valid without collisions."""
        for col_idx, row_idx in piece.get_world_blocks():
            target_x = col_idx + offset_x
            target_y = row_idx + offset_y

            # Check horizontal boundaries
            if target_x < 0 or target_x >= self.width:
                return False

            # Check bottom boundary
            if target_y >= self.height:
                return False

            # Check existing locked blocks (ignoring above top ceiling)
            if target_y >= 0 and self.grid[target_y][target_x] is not None:
                return False

        return True

    def lock_piece(self, piece: "Piece") -> None:
        """Locks the given piece permanently into the board grid."""
        for x, y in piece.get_world_blocks():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = piece.color

    def clear_full_lines(self) -> int:
        """Iterates through all rows, removes completed lines, and shifts rows down.
        Returns the total count of lines cleared.
        """
        lines_cleared = 0
        r = self.height - 1
        while r >= 0:
            if self.is_line_full(r):
                self.clear_line(r)
                self.move_rows_down(r)
                lines_cleared += 1
            else:
                r -= 1
        return lines_cleared

    def is_line_full(self, row: int) -> bool:
        """Returns True if every cell in the specified row is occupied."""
        if 0 <= row < self.height:
            return all(cell is not None for cell in self.grid[row])
        return False

    def clear_line(self, row: int) -> None:
        """Clears all cells in a single row."""
        if 0 <= row < self.height:
            self.grid[row] = [None for _ in range(self.width)]

    def move_rows_down(self, from_row: int) -> None:
        """Shifts all rows above from_row down by one grid cell."""
        for r in range(from_row, 0, -1):
            self.grid[r] = self.grid[r - 1][:]
        self.grid[0] = [None for _ in range(self.width)]

    def reset(self) -> None:
        """Clears the entire board grid back to empty cells."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]