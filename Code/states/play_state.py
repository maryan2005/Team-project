import random
from typing import Optional, TYPE_CHECKING
import pygame
from states.base_state import GameState
from domain.board import Board
from domain.piece import Piece, TETROMINO_SHAPES
from domain.interfaces import IScoreManager, IChallengeManager
from domain.score_manager import GuidelineScoreManager
from domain.challenge_manager import StandardChallengeManager
from domain.high_score_repository import FileHighScoreRepository
from input.interfaces import IInputHandler
from input.input_handler import InputHandler
from rendering.board_renderer import BoardRenderer

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class PlayState(GameState):
    """Core play state coordinating input, board grid updates, piece collisions,
    scoring, and rendering based on tetris_ver2 mechanics.
    """

    def __init__(self, engine: "GameEngine") -> None:
        super().__init__(engine)
        self.board: Board = Board(width=10, height=20)
        
        # Initialize active and next piece using letter keys matching piece.py
        self.active_piece: Piece = Piece(shape_type=self._get_random_shape_type(), x=3, y=0)
        self.next_piece: Piece = Piece(shape_type=self._get_random_shape_type(), x=3, y=0)
        self.held_piece: Optional[Piece] = None
        self.can_hold: bool = True

        # Annotated strictly using abstract interface contracts per UML diagram
        self.input_handler: IInputHandler = InputHandler(self.engine.settings_manager)
        self.score_manager: IScoreManager = GuidelineScoreManager(FileHighScoreRepository())
        self.challenge_manager: IChallengeManager = StandardChallengeManager()
        self.board_renderer: BoardRenderer = BoardRenderer(cell_size=20, grid_offset_x=100, grid_offset_y=60)

        # Seconds since the piece last fell, and whether Down is held
        self.fall_timer: float = 0.0
        self.pressing_down: bool = False

        self.font = pygame.font.SysFont("Calibri", 25, bold=True)

    def _get_random_shape_type(self) -> str:
        """Picks a random shape key string matching TETROMINO_SHAPES keys ("I", "J", "L", etc.)."""
        return random.choice(list(TETROMINO_SHAPES.keys()))

    def spawn_next_piece(self) -> None:
        """Promotes next_piece to active_piece and generates a replacement for next_piece.
        Triggers Game Over if newly promoted active piece instantly collides.
        """
        self.active_piece = self.next_piece
        self.active_piece.reset_position()
        self.next_piece = Piece(shape_type=self._get_random_shape_type(), x=3, y=0)

        if not self.board.is_valid_position(self.active_piece):
            self.game_over()

    def handle_input(self, event: pygame.event.Event) -> None:
        """Processes discrete keyboard input events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause_game()
            return

        action = self.input_handler.process_event(event)

        if action == "rotate":
            self.active_piece.rotate_cw()
            if not self.board.is_valid_position(self.active_piece):
                self.active_piece.rotate_ccw()

        elif action == "move_left":
            self.go_side(-1)

        elif action == "move_right":
            self.go_side(1)

        elif action == "hard_drop":
            self.go_space()

        elif action == "soft_drop":
            self.pressing_down = True

        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            self.pressing_down = False

    def go_side(self, dx: int) -> None:
        """Shifts active piece horizontally if target position is valid."""
        old_x = self.active_piece.x
        self.active_piece.move(dx, 0)
        if not self.board.is_valid_position(self.active_piece):
            self.active_piece.x = old_x

    def go_down(self) -> None:
        """Moves active piece down by 1 row; freezes piece upon collision."""
        self.active_piece.move(0, 1)
        if not self.board.is_valid_position(self.active_piece):
            self.active_piece.move(0, -1)
            self.freeze()

    def go_space(self) -> None:
        """Instantly drops active piece to bottom-most valid position."""
        start_y = self.active_piece.y
        while self.board.is_valid_position(self.active_piece, offset_y=1):
            self.active_piece.move(0, 1)
        # Score before freeze(), which replaces the active piece
        self.score_manager.add_drop_score(self.active_piece.y - start_y, is_hard_drop=True)
        self.freeze()

    def freeze(self) -> None:
        """Locks active piece into field, calculates cleared lines, updates score,
        and spawns next figure from queue.
        """
        self.board.lock_piece(self.active_piece)
        lines_cleared = self.board.clear_full_lines()
        # Always report the lock, even with 0 lines, so a combo can reset
        self.score_manager.process_line_clear(lines_cleared)

        self.spawn_next_piece()

    def hold_piece_action(self) -> None:
        """Stub method satisfying PlayState interface."""
        pass

    def update(self, delta_time: float) -> None:
        """Updates game tick loop and automatic fall movement."""
        # Fall one row each time the level's fall speed has passed
        self.fall_timer += delta_time
        time_to_fall = self.fall_timer >= self.score_manager.get_fall_speed()
        if time_to_fall:
            self.fall_timer = 0.0
        if time_to_fall or self.pressing_down:
            start_y = self.active_piece.y
            self.go_down()
            # Only the player's soft drop scores, not gravity or landing
            if self.pressing_down and self.active_piece.y > start_y:
                self.score_manager.add_drop_score(1, is_hard_drop=False)

        self.challenge_manager.update(
            delta_time=delta_time,
            current_score=self.score_manager.get_score(),
            lines_cleared=self.score_manager.get_lines()
        )

    def draw(self, surface: pygame.Surface) -> None:
        """Renders grid field, active piece, and current score banner."""
        self.board_renderer.render_board(surface, self.board)
        self.board_renderer.render_piece(surface, self.active_piece)

        # Render score banner at top-left corner
        score_text = self.font.render(f"Score: {self.score_manager.get_score()}", True, (0, 0, 0))
        surface.blit(score_text, (0, 0))
        level_text = self.font.render(f"Level: {self.score_manager.get_level()}", True, (0, 0, 0))
        surface.blit(level_text, (0, 30))

    def pause_game(self) -> None:
        """Transitions to PauseState while passing self as suspended state."""
        from states.pause_state import PauseState
        self.engine.change_state(PauseState(self.engine, self))

    def game_over(self) -> None:
        """Saves the final score, then transitions to GameOverState."""
        from states.game_over_state import GameOverState
        game_over_state = GameOverState(self.engine)
        game_over_state.is_high_score = self.score_manager.save_final_score()
        game_over_state.final_score = self.score_manager.get_score()
        game_over_state.lines_cleared = self.score_manager.get_lines()
        game_over_state.leaderboard = self.score_manager.get_leaderboard()
        self.engine.change_state(game_over_state)
        
