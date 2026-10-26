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
        self.preview_font: pygame.font.Font = pygame.font.SysFont("Calibri", 20, bold=True)

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
        """Renders a solid active piece or an outlined ghost piece."""
        for x, y in piece.get_world_blocks():
            block_rect = [
                self.grid_offset_x + self.cell_size * x + 1,
                self.grid_offset_y + self.cell_size * y + 1,
                self.cell_size - 2,
                self.cell_size - 2,
            ]
            if is_ghost:
                pygame.draw.rect(surface, piece.color, block_rect, 2)
            else:
                pygame.draw.rect(surface, piece.color, block_rect)

    def render_hold_and_next(self, surface: pygame.Surface, held_piece: Optional[Piece], next_piece: Piece) -> None:
        """Draws the held and upcoming pieces in panels beside the playfield."""
        panel_width = 140
        hold_x = self.grid_offset_x + self.cell_size * 10 + 24
        next_x = hold_x + panel_width + 16
        self._render_preview(surface, "HOLD", held_piece, hold_x, panel_width)
        self._render_preview(surface, "NEXT", next_piece, next_x, panel_width)

    def _render_preview(
        self,
        surface: pygame.Surface,
        label: str,
        piece: Optional[Piece],
        panel_x: int,
        panel_width: int,
    ) -> None:
        label_surface = self.preview_font.render(label, True, (0, 0, 0))
        surface.blit(label_surface, (panel_x, self.grid_offset_y))
        if piece is None:
            return

        occupied = [
            (column, row)
            for row, cells in enumerate(piece.shape)
            for column, cell in enumerate(cells)
            if cell
        ]
        if not occupied:
            return

        min_column = min(column for column, _ in occupied)
        max_column = max(column for column, _ in occupied)
        min_row = min(row for _, row in occupied)
        max_row = max(row for _, row in occupied)
        preview_cell_size = max(12, self.cell_size - 4)
        piece_width = (max_column - min_column + 1) * preview_cell_size
        piece_height = (max_row - min_row + 1) * preview_cell_size
        preview_x = panel_x + (panel_width - piece_width) // 2
        preview_y = self.grid_offset_y + 36 + (4 * preview_cell_size - piece_height) // 2

        for column, row in occupied:
            block_rect = [
                preview_x + (column - min_column) * preview_cell_size,
                preview_y + (row - min_row) * preview_cell_size,
                preview_cell_size - 1,
                preview_cell_size - 1,
            ]
            pygame.draw.rect(surface, piece.color, block_rect)