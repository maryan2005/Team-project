from typing import Optional
import pygame
from domain.board import Board
from domain.piece import Piece


class BoardRenderer:
    """Renders the grid board and active pieces based on tetris_ver2 layout constants."""

    def __init__(self, cell_size: int = 20, grid_offset_x: int = 100, grid_offset_y: int = 60) -> None:
        self.cell_size: int = cell_size
        self.grid_offset_x: int = grid_offset_x
        self.grid_offset_y: int = grid_offset_y

    def render_board(self, surface: pygame.Surface, board: Board) -> None:
        """Draws the grid background, cell outlines, and locked blocks."""
        surface.fill((255, 255, 255))  # White background matching tetris_ver2

        for i in range(board.height):
            for j in range(board.width):
                # Cell outline
                cell_rect = [
                    self.grid_offset_x + self.cell_size * j,
                    self.grid_offset_y + self.cell_size * i,
                    self.cell_size,
                    self.cell_size,
                ]
                pygame.draw.rect(surface, (128, 128, 128), cell_rect, 1)

                # Locked block fill
                color = board.grid[i][j]
                if color is not None:
                    block_rect = [
                        self.grid_offset_x + self.cell_size * j + 1,
                        self.grid_offset_y + self.cell_size * i + 1,
                        self.cell_size - 2,
                        self.cell_size - 1,
                    ]
                    pygame.draw.rect(surface, color, block_rect)

    def render_piece(self, surface: pygame.Surface, piece: Piece, is_ghost: bool = False) -> None:
        """Renders the active falling piece blocks."""
        for x, y in piece.get_world_blocks():
            block_rect = [
                self.grid_offset_x + self.cell_size * x + 1,
                self.grid_offset_y + self.cell_size * y + 1,
                self.cell_size - 2,
                self.cell_size - 2,
            ]
            pygame.draw.rect(surface, piece.color, block_rect)

    def render_hold_and_next(self, surface: pygame.Surface, held_piece: Optional[Piece], next_piece: Piece) -> None:
        """Stub method satisfying the BoardRenderer interface (tetris_ver2 lacks previews)."""
        pass