import pygame

from states.play_state import PlayState


class FakeInputHandler:
    def update_held_inputs(self, delta_time):
        return []

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            return "soft_drop"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            return "move_left"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            return "rotate"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            return "rotate_ccw"
        return None


class FakeScoreManager:
    def __init__(self):
        self.drop_scores = []
        self.fall_speed = 10.0

    def get_fall_speed(self):
        return self.fall_speed

    def add_drop_score(self, distance, is_hard_drop):
        self.drop_scores.append((distance, is_hard_drop))

    def get_score(self):
        return 0

    def get_lines(self):
        return 0


class FakeChallengeManager:
    def update(self, **kwargs):
        pass


class FakePiece:
    def __init__(self, shape_type="T"):
        self.shape_type = shape_type
        self.x = 0
        self.y = 0
        self.rotation_index = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate_cw(self):
        self.rotation_index = (self.rotation_index + 1) % 4

    def rotate_ccw(self):
        self.rotation_index = (self.rotation_index - 1) % 4


class FakeBoard:
    def __init__(self):
        self.grounded = False
        self.invalid_positions = set()

    def is_valid_position(self, piece, offset_x=0, offset_y=0):
        target = (piece.x + offset_x, piece.y + offset_y)
        return target not in self.invalid_positions and not (
            self.grounded and offset_y > 0
        )


def make_play_state(shape_type="T"):
    state = PlayState.__new__(PlayState)
    state.input_handler = FakeInputHandler()
    state.score_manager = FakeScoreManager()
    state.challenge_manager = FakeChallengeManager()
    state.fall_timer = 0.0
    state.soft_drop_timer = 0.0
    state.lock_timer = 0.0
    state.lock_delay_resets = 0
    state.pressing_down = False
    state.active_piece = FakePiece(shape_type)
    state.board = FakeBoard()
    state.down_steps = 0

    def go_down():
        state.down_steps += 1
        state.active_piece.y += 1

    state.go_down = go_down
    return state


def test_soft_drop_moves_immediately_then_at_timed_interval():
    state = make_play_state()
    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))

    state.update(0.0)
    assert state.down_steps == 1

    state.update(0.049)
    assert state.down_steps == 1
    state.update(0.001)
    assert state.down_steps == 2
    assert state.score_manager.drop_scores == [(1, False), (1, False)]


def test_soft_drop_catches_up_for_elapsed_time():
    state = make_play_state()
    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))

    state.update(0.2)

    assert state.down_steps == 5
    assert state.score_manager.drop_scores == [(1, False)] * 5


def test_releasing_soft_drop_clears_timer_and_stops_steps():
    state = make_play_state()
    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
    state.handle_input(pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN))

    state.update(1.0)

    assert state.down_steps == 0
    assert state.soft_drop_timer == 0.0


def test_gravity_does_not_add_an_extra_step_when_soft_drop_is_due():
    state = make_play_state()
    state.score_manager.fall_speed = PlayState.SOFT_DROP_INTERVAL
    state.fall_timer = PlayState.SOFT_DROP_INTERVAL
    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))

    state.update(0.0)

    assert state.down_steps == 1
    assert state.score_manager.drop_scores == [(1, False)]


def test_gravity_preserves_elapsed_time_after_a_fall_tick():
    state = make_play_state()
    state.score_manager.fall_speed = 0.5

    state.update(0.6)
    assert state.down_steps == 1
    assert abs(state.fall_timer - 0.1) < 1e-9

    state.update(0.39)
    assert state.down_steps == 1

    state.update(0.02)
    assert state.down_steps == 2


def test_grounded_piece_locks_only_after_lock_delay():
    state = make_play_state()
    state.board.grounded = True
    locked = []
    state.freeze = lambda: locked.append(True)

    state.update(PlayState.LOCK_DELAY_SECONDS - 0.01)
    assert locked == []
    state.update(0.01)
    assert locked == [True]


def test_grounded_horizontal_move_resets_lock_timer_up_to_limit():
    state = make_play_state()
    state.board.grounded = True
    state.lock_timer = 0.3

    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
    assert state.lock_timer == 0.0
    assert state.lock_delay_resets == 1

    state.lock_timer = 0.3
    state.lock_delay_resets = PlayState.MAX_LOCK_DELAY_RESETS
    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
    assert state.lock_timer == 0.3
    assert state.lock_delay_resets == PlayState.MAX_LOCK_DELAY_RESETS


def test_grounded_rotation_resets_lock_timer():
    state = make_play_state()
    state.board.grounded = True
    state.lock_timer = 0.3

    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))

    assert state.lock_timer == 0.0
    assert state.lock_delay_resets == 1


def test_clockwise_rotation_uses_first_valid_jlstz_wall_kick():
    state = make_play_state()
    state.board.invalid_positions.add((0, 0))

    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))

    assert (state.active_piece.x, state.active_piece.y) == (-1, 0)
    assert state.active_piece.rotation_index == 1


def test_i_piece_uses_its_srs_kick_tests():
    state = make_play_state(shape_type="I")
    state.board.invalid_positions.add((0, 0))

    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))

    assert (state.active_piece.x, state.active_piece.y) == (-2, 0)
    assert state.active_piece.rotation_index == 1


def test_srs_clockwise_kick_offsets_cover_each_rotation_transition():
    expected_offsets = {
        "T": [(-1, 0), (1, 0), (1, 0), (-1, 0)],
        "I": [(-2, 0), (-1, 0), (2, 0), (1, 0)],
    }
    for shape_type, offsets in expected_offsets.items():
        for start_rotation, expected_offset in enumerate(offsets):
            state = make_play_state(shape_type=shape_type)
            state.active_piece.rotation_index = start_rotation
            state.board.invalid_positions.add((0, 0))

            assert state._rotate_piece_with_kicks()
            assert (state.active_piece.x, state.active_piece.y) == expected_offset
            assert state.active_piece.rotation_index == (start_rotation + 1) % 4


def test_rotation_is_reverted_when_all_srs_kicks_fail():
    state = make_play_state()
    state.board.invalid_positions.update(
        {(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)}
    )

    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))

    assert (state.active_piece.x, state.active_piece.y) == (0, 0)
    assert state.active_piece.rotation_index == 0


def test_counterclockwise_rotation_uses_srs_wall_kick():
    state = make_play_state()
    state.board.invalid_positions.add((0, 0))

    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z))

    assert (state.active_piece.x, state.active_piece.y) == (1, 0)
    assert state.active_piece.rotation_index == 3


def test_counterclockwise_kick_offsets_cover_each_rotation_transition():
    expected_offsets = {
        "T": [(1, 0), (1, 0), (-1, 0), (-1, 0)],
        "I": [(1, 0), (1, 0), (-2, 0), (-1, 0)],
    }
    for shape_type, offsets in expected_offsets.items():
        for start_rotation, expected_offset in enumerate(offsets):
            state = make_play_state(shape_type=shape_type)
            state.active_piece.rotation_index = start_rotation
            state.board.invalid_positions.add((0, 0))

            state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z))

            assert (state.active_piece.x, state.active_piece.y) == expected_offset
            assert state.active_piece.rotation_index == (start_rotation - 1) % 4


def test_counterclockwise_rotation_reverts_if_all_kicks_fail():
    state = make_play_state()
    state.board.invalid_positions.update(
        {(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)}
    )

    state.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z))

    assert (state.active_piece.x, state.active_piece.y) == (0, 0)
    assert state.active_piece.rotation_index == 0
