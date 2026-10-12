import random
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING
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


# Offsets use board coordinates, where positive y points down.
_JLSTZ_CW_KICKS: Dict[Tuple[int, int], List[Tuple[int, int]]] = {
    (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (1, 2): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (2, 3): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
}

_I_CW_KICKS: Dict[Tuple[int, int], List[Tuple[int, int]]] = {
    (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
}

_JLSTZ_CCW_KICKS: Dict[Tuple[int, int], List[Tuple[int, int]]] = {
    (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
}

_I_CCW_KICKS: Dict[Tuple[int, int], List[Tuple[int, int]]] = {
    (0, 3): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (1, 0): [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
    (2, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (3, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
}


class PlayState(GameState):
    """Core play state coordinating input, board grid updates, piece collisions,
    scoring, and rendering based on tetris_ver2 mechanics.
    """

    SOFT_DROP_INTERVAL: float = 0.05
    LOCK_DELAY_SECONDS: float = 0.5
    MAX_LOCK_DELAY_RESETS: int = 15

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
        self.soft_drop_timer: float = 0.0
        self.lock_timer: float = 0.0
        self.lock_delay_resets: int = 0
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
        self.lock_timer = 0.0
        self.lock_delay_resets = 0

        if not self.board.is_valid_position(self.active_piece):
            self.game_over()

    def handle_input(self, event: pygame.event.Event) -> None:
        """Processes discrete keyboard input events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause_game()
            return

        action = self.input_handler.process_event(event)

        if action == "rotate":
            was_grounded = self._is_grounded()
            if self._rotate_piece_with_kicks(clockwise=True):
                self._reset_lock_delay_for_player_action(was_grounded)

        elif action == "rotate_ccw":
            was_grounded = self._is_grounded()
            if self._rotate_piece_with_kicks(clockwise=False):
                self._reset_lock_delay_for_player_action(was_grounded)

        elif action == "move_left":
            self.go_side(-1)

        elif action == "move_right":
            self.go_side(1)

        elif action == "hard_drop":
            self.go_space()

        elif action == "soft_drop":
            if not self.pressing_down:
                self.soft_drop_timer = self.SOFT_DROP_INTERVAL
            self.pressing_down = True

        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            self.pressing_down = False
            self.soft_drop_timer = 0.0

    def go_side(self, dx: int) -> None:
        """Shifts active piece horizontally if target position is valid."""
        was_grounded = self._is_grounded()
        old_x = self.active_piece.x
        self.active_piece.move(dx, 0)
        if not self.board.is_valid_position(self.active_piece):
            self.active_piece.x = old_x
        else:
            self._reset_lock_delay_for_player_action(was_grounded)

    def go_down(self) -> None:
        """Moves active piece down by one row if the next position is valid."""
        self.active_piece.move(0, 1)
        if not self.board.is_valid_position(self.active_piece):
            self.active_piece.move(0, -1)

    def _is_grounded(self) -> bool:
        """Returns whether the active piece cannot move down one more row."""
        return not self.board.is_valid_position(self.active_piece, offset_y=1)

    def _rotate_piece_with_kicks(self, clockwise: bool = True) -> bool:
        """Rotates using SRS kick tests, restoring state if all tests fail."""
        piece = self.active_piece
        from_rotation = piece.rotation_index
        to_rotation = (from_rotation + (1 if clockwise else -1)) % 4
        if piece.shape_type == "O":
            kick_tests = [(0, 0)]
        elif piece.shape_type == "I":
            kick_table = _I_CW_KICKS if clockwise else _I_CCW_KICKS
            kick_tests = kick_table[(from_rotation, to_rotation)]
        else:
            kick_table = _JLSTZ_CW_KICKS if clockwise else _JLSTZ_CCW_KICKS
            kick_tests = kick_table[(from_rotation, to_rotation)]

        original_x, original_y = piece.x, piece.y
        if clockwise:
            piece.rotate_cw()
        else:
            piece.rotate_ccw()
        for offset_x, offset_y in kick_tests:
            piece.x = original_x + offset_x
            piece.y = original_y + offset_y
            if self.board.is_valid_position(piece):
                return True

        piece.x, piece.y = original_x, original_y
        if clockwise:
            piece.rotate_ccw()
        else:
            piece.rotate_cw()
        return False

    def _reset_lock_delay_for_player_action(self, was_grounded: bool) -> None:
        """Resets lock delay after successful grounded movement, up to the reset cap."""
        if was_grounded and self.lock_delay_resets < self.MAX_LOCK_DELAY_RESETS:
            self.lock_timer = 0.0
            self.lock_delay_resets += 1

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
        soft_drop_tick_processed = False
        for action in self.input_handler.update_held_inputs(delta_time):
            if action == "move_left":
                self.go_side(-1)
            elif action == "move_right":
                self.go_side(1)

        if self.pressing_down:
            self.soft_drop_timer += max(0.0, delta_time)
            while self.soft_drop_timer >= self.SOFT_DROP_INTERVAL:
                self.soft_drop_timer -= self.SOFT_DROP_INTERVAL
                soft_drop_tick_processed = True
                piece_before_drop = self.active_piece
                start_y = piece_before_drop.y
                self.go_down()
                if self.active_piece is not piece_before_drop:
                    self.soft_drop_timer = 0.0
                    break
                if self.active_piece.y > start_y:
                    self.score_manager.add_drop_score(1, is_hard_drop=False)

        # Fall one row each time the level's fall speed has passed
        self.fall_timer += delta_time
        fall_interval = self.score_manager.get_fall_speed()
        time_to_fall = self.fall_timer >= fall_interval
        if time_to_fall:
            self.fall_timer -= fall_interval
        if time_to_fall and not soft_drop_tick_processed:
            self.go_down()

        if self._is_grounded():
            self.lock_timer += max(0.0, delta_time)
            if self.lock_timer >= self.LOCK_DELAY_SECONDS:
                self.freeze()
        else:
            self.lock_timer = 0.0

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
        
