import pygame

from domain.board import Board
from domain.piece import Piece
from rendering.board_renderer import BoardRenderer
from states.play_state import PlayState


def make_play_state():
    state = PlayState.__new__(PlayState)
    state.board = Board()
    state.active_piece = Piece("T", x=4, y=5)
    state.next_piece = Piece("I")
    state.held_piece = None
    state.can_hold = True
    state.fall_timer = 1.0
    state.soft_drop_timer = 0.2
    state.lock_timer = 0.3
    state.lock_delay_resets = 2
    state._get_random_shape_type = lambda: "L"
    state.game_over = lambda: None
    return state


def test_first_hold_stores_active_piece_and_promotes_next():
    state = make_play_state()
    outgoing_piece = state.active_piece

    state.hold_piece_action()

    assert state.held_piece is outgoing_piece
    assert (state.held_piece.x, state.held_piece.y) == (3, 0)
    assert state.held_piece.rotation_index == 0
    assert state.active_piece.shape_type == "I"
    assert state.next_piece.shape_type == "L"
    assert state.can_hold is False
    assert state.fall_timer == 0.0
    assert state.soft_drop_timer == 0.0
    assert state.lock_timer == 0.0
    assert state.lock_delay_resets == 0


def test_hold_swaps_with_stored_piece_and_cannot_repeat_until_new_piece():
    state = make_play_state()
    held_piece = Piece("O", x=7, y=12)
    held_piece.rotate_cw()
    state.held_piece = held_piece
    outgoing_piece = state.active_piece
    state.active_piece.rotate_cw()
    state.can_hold = True

    state.hold_piece_action()

    assert state.active_piece is held_piece
    assert (state.active_piece.x, state.active_piece.y) == (3, 0)
    assert state.active_piece.rotation_index == 0
    assert state.held_piece is outgoing_piece
    assert (state.held_piece.x, state.held_piece.y) == (3, 0)
    assert state.held_piece.rotation_index == 0
    assert state.can_hold is False

    next_active_piece = state.active_piece
    state.hold_piece_action()
    assert state.active_piece is next_active_piece
    assert state.held_piece is outgoing_piece


def test_spawn_next_piece_reenables_hold():
    state = make_play_state()
    state.can_hold = False
    state.spawn_next_piece()

    assert state.can_hold is True
    assert state.active_piece.shape_type == "I"
    assert state.next_piece.shape_type == "L"


def test_draw_renders_ghost_before_active_piece_and_hold_next_previews():
    pygame.font.init()

    class RecordingRenderer:
        def __init__(self):
            self.pieces = []
            self.previews = None

        def render_board(self, surface, board):
            pass

        def render_piece(self, surface, piece, is_ghost=False):
            self.pieces.append((piece, is_ghost))

        def render_hold_and_next(self, surface, held_piece, next_piece):
            self.previews = (held_piece, next_piece)

    class ScoreManager:
        def get_score(self):
            return 0

        def get_level(self):
            return 1

    state = make_play_state()
    renderer = RecordingRenderer()
    state.board_renderer = renderer
    state.font = pygame.font.SysFont("Calibri", 25, bold=True)
    state.score_manager = ScoreManager()
    surface = pygame.Surface((800, 600))
    active_x, active_y = state.active_piece.x, state.active_piece.y

    state.draw(surface)

    ghost_piece, is_ghost = renderer.pieces[0]
    assert is_ghost is True
    assert (ghost_piece.x, ghost_piece.y) == state.active_piece.get_ghost_position(state.board)
    assert renderer.pieces[1] == (state.active_piece, False)
    assert (state.active_piece.x, state.active_piece.y) == (active_x, active_y)
    assert renderer.previews == (None, state.next_piece)


def test_renderer_draws_ghost_outline_and_held_next_previews():
    pygame.font.init()
    surface = pygame.Surface((800, 600))
    surface.fill((255, 255, 255))
    renderer = BoardRenderer()

    renderer.render_piece(surface, Piece("O", x=0, y=0), is_ghost=True)
    renderer.render_hold_and_next(surface, Piece("T"), Piece("I"))

    assert surface.get_at((101, 61))[:3] == Piece("O").color
    assert surface.get_at((110, 70))[:3] == (255, 255, 255)
    assert surface.get_at((386, 116))[:3] == Piece("T").color
    assert surface.get_at((518, 120))[:3] == Piece("I").color
