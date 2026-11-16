from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.board import Board

# Standard Tetromino Shapes (0 and 1 matrices)
TETROMINO_SHAPES = {
    "I": [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    "J": [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    "L": [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ],
    "O": [
        [1, 1],
        [1, 1]
    ],
    "S": [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],
    "T": [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    "Z": [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
}

# Standard Tetromino RGB Colors
TETROMINO_COLORS = {
    "I": (0, 240, 240),    # Cyan
    "J": (0, 0, 240),      # Blue
    "L": (240, 160, 0),    # Orange
    "O": (240, 240, 0),    # Yellow
    "S": (0, 240, 0),      # Green
    "T": (160, 0, 240),    # Purple
    "Z": (240, 0, 0)       # Red
}


class Piece:
    """Represents a falling Tetromino piece matching the UML specification verbatim."""

    def __init__(self, shape_type: str, x: int = 3, y: int = 0) -> None:
        self.shape_type: str = shape_type
        self.shape: List[List[int]] = [row[:] for row in TETROMINO_SHAPES[shape_type]]
        self.color: Tuple[int, int, int] = TETROMINO_COLORS[shape_type]
        self.x: int = x
        self.y: int = y
        self.rotation_index: int = 0

    def move(self, dx: int, dy: int) -> None:
        """Shifts the piece by dx and dy in world coordinates."""
        self.x += dx
        self.y += dy

    def rotate_cw(self) -> None:
        """Rotates the shape matrix 90 degrees clockwise."""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.rotation_index = (self.rotation_index + 1) % 4

    def rotate_ccw(self) -> None:
        """Rotates the shape matrix 90 degrees counter-clockwise."""
        self.shape = [list(row) for row in zip(*self.shape)][::-1]
        self.rotation_index = (self.rotation_index - 1) % 4

    def get_world_blocks(self) -> List[Tuple[int, int]]:
        """Returns global grid coordinates (x, y) for occupied cells."""
        blocks: List[Tuple[int, int]] = []
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + col_idx, self.y + row_idx))
        return blocks

    def get_ghost_position(self, board: "Board") -> Tuple[int, int]:
        """Calculates and returns the target (x, y) coordinates of the ghost piece
        by simulating dropping down until encountering a collision on the board.
        """
        ghost_x = self.x
        ghost_y = self.y

        while board.is_valid_position(self, offset_x=ghost_x - self.x, offset_y=(ghost_y - self.y) + 1):
            ghost_y += 1

        return (ghost_x, ghost_y)

    def reset_position(self) -> None:
        """Resets position and rotation state back to spawn defaults."""
        self.x = 3
        self.y = 0
        self.rotation_index = 0
        self.shape = [row[:] for row in TETROMINO_SHAPES[self.shape_type]]