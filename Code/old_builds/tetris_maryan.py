import pygame
import random
import json
import os


pygame.init()


CELL_SIZE = 25
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_X = 30
BOARD_Y = 80
PANEL_X = 310
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 620
FPS = 60
HIGH_SCORE_FILE = "tetris_high_scores.json"


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (35, 35, 35)
CYAN = (0, 220, 220)
YELLOW = (240, 220, 0)
PURPLE = (160, 60, 220)
GREEN = (40, 200, 80)
RED = (230, 50, 50)
BLUE = (50, 100, 240)
ORANGE = (255, 150, 30)


COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]


SHAPES = [
    [(0, 1), (1, 1), (2, 1), (3, 1)],
    [(1, 0), (2, 0), (1, 1), (2, 1)],
    [(1, 0), (0, 1), (1, 1), (2, 1)],
    [(1, 0), (2, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(2, 0), (0, 1), (1, 1), (2, 1)]
]


DIFFICULTIES = {
    "Easy": {"speed": 800, "multiplier": 1},
    "Normal": {"speed": 600, "multiplier": 1.25},
    "Hard": {"speed": 400, "multiplier": 1.5}
}


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()


FONT = pygame.font.SysFont("Arial", 18)
MEDIUM_FONT = pygame.font.SysFont("Arial", 26)
TITLE_FONT = pygame.font.SysFont("Arial", 48)


def load_leaderboard():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return []


def save_leaderboard(board):
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            json.dump(board[:5], file, indent=2)
    except OSError:
        pass


leaderboard = load_leaderboard()


def draw_text(text, font, color, x, y, center=False):
    image = font.render(str(text), True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def draw_centered_lines(lines, font, color, start_y, gap=35):
    for index, line in enumerate(lines):
        draw_text(line, font, color, SCREEN_WIDTH // 2,
                  start_y + index * gap, True)


def new_piece():
    shape_id = random.randrange(len(SHAPES))
    return {
        "shape": shape_id,
        "cells": SHAPES[shape_id][:],
        "color": COLORS[shape_id],
        "x": 3,
        "y": 0
    }


def rotate_cells(cells):
    return [(3 - y, x) for x, y in cells]


def create_game(difficulty):
    return {
        "board": [[None for _ in range(BOARD_WIDTH)]
                  for _ in range(BOARD_HEIGHT)],
        "piece": new_piece(),
        "score": 0,
        "lines": 0,
        "level": 1,
        "combo": -1,
        "back_to_back": False,
        "stats": {
            "single": 0,
            "double": 0,
            "triple": 0,
            "tetris": 0
        },
        "difficulty": difficulty,
        "fall_timer": 0,
        "soft_timer": 0,
        "saved": False
    }


def collides(game, piece, dx=0, dy=0, cells=None):
    if cells is None:
        cells = piece["cells"]


    board = game["board"]


    for x, y in cells:
        board_x = piece["x"] + x + dx
        board_y = piece["y"] + y + dy


        if board_x < 0 or board_x >= BOARD_WIDTH:
            return True


        if board_y >= BOARD_HEIGHT:
            return True


        if board_y >= 0 and board[board_y][board_x] is not None:
            return True


    return False


def move_piece(game, dx, dy):
    piece = game["piece"]


    if not collides(game, piece, dx, dy):
        piece["x"] += dx
        piece["y"] += dy
        return True


    return False


def rotate_piece(game):
    piece = game["piece"]
    rotated = rotate_cells(piece["cells"])


    if not collides(game, piece, cells=rotated):
        piece["cells"] = rotated
        return


    for offset in [-1, 1, -2, 2]:
        if not collides(game, piece, offset, 0, rotated):
            piece["x"] += offset
            piece["cells"] = rotated
            return


def update_score(game, points):
    multiplier = DIFFICULTIES[game["difficulty"]]["multiplier"]
    game["score"] += round(points * game["level"] * multiplier)


def clear_lines(game):
    board = game["board"]
    remaining = [row for row in board if any(cell is None for cell in row)]
    cleared = BOARD_HEIGHT - len(remaining)


    if cleared:
        empty_rows = [
            [None for _ in range(BOARD_WIDTH)]
            for _ in range(cleared)
        ]
        game["board"] = empty_rows + remaining
        game["lines"] += cleared


        game["stats"][{
            1: "single",
            2: "double",
            3: "triple",
            4: "tetris"
        }[cleared]] += 1


        points = {1: 100, 2: 200, 3: 300, 4: 400}
        update_score(game, points[cleared])


        game["combo"] += 1
        if game["combo"] > 0:
            update_score(game, 50 * game["combo"])


        if cleared == 4:
            if game["back_to_back"]:
                update_score(game, 200)
            game["back_to_back"] = True
        else:
            game["back_to_back"] = False


        game["level"] = game["lines"] // 10 + 1


    else:
        game["combo"] = -1


    return cleared


def lock_piece(game):
    piece = game["piece"]


    for x, y in piece["cells"]:
        board_x = piece["x"] + x
        board_y = piece["y"] + y


        if board_y < 0:
            return False


        game["board"][board_y][board_x] = piece["color"]


    clear_lines(game)
    game["piece"] = new_piece()


    if collides(game, game["piece"]):
        return False


    return True


def hard_drop(game):
    distance = 0


    while move_piece(game, 0, 1):
        distance += 1


    update_score(game, distance * 2)
    return lock_piece(game)


def get_fall_speed(game):
    base_speed = DIFFICULTIES[game["difficulty"]]["speed"]
    return max(80, base_speed - (game["level"] - 1) * 50)


def finish_game(game):
    if game["saved"]:
        return


    leaderboard.append({
        "score": game["score"],
        "level": game["level"],
        "difficulty": game["difficulty"],
        "lines": game["lines"]
    })


    leaderboard.sort(key=lambda entry: entry["score"], reverse=True)
    del leaderboard[5:]
    save_leaderboard(leaderboard)
    game["saved"] = True


def draw_board(game):
    screen.fill(BLACK)


    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            rect = (
                BOARD_X + x * CELL_SIZE,
                BOARD_Y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )


            pygame.draw.rect(screen, GRAY, rect, 1)


            color = game["board"][y][x]
            if color is not None:
                pygame.draw.rect(
                    screen,
                    color,
                    (rect[0] + 1, rect[1] + 1,
                     CELL_SIZE - 2, CELL_SIZE - 2)
                )


    piece = game["piece"]
    for x, y in piece["cells"]:
        px = BOARD_X + (piece["x"] + x) * CELL_SIZE
        py = BOARD_Y + (piece["y"] + y) * CELL_SIZE


        if py >= BOARD_Y:
            pygame.draw.rect(
                screen,
                piece["color"],
                (px + 1, py + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            )


    pygame.draw.rect(
        screen,
        WHITE,
        (BOARD_X, BOARD_Y,
         BOARD_WIDTH * CELL_SIZE,
         BOARD_HEIGHT * CELL_SIZE),
        2
    )


    draw_text("TETRIS", MEDIUM_FONT, WHITE, PANEL_X, 25)
    draw_text("Score", FONT, WHITE, PANEL_X, 90)
    draw_text(game["score"], MEDIUM_FONT, YELLOW, PANEL_X, 115)
    draw_text("High Score", FONT, WHITE, PANEL_X, 155)


    high_score = leaderboard[0]["score"] if leaderboard else 0
    draw_text(high_score, MEDIUM_FONT, YELLOW, PANEL_X, 180)


    draw_text("Level", FONT, WHITE, PANEL_X, 225)
    draw_text(game["level"], MEDIUM_FONT, CYAN, PANEL_X, 250)
    draw_text("Lines", FONT, WHITE, PANEL_X, 290)
    draw_text(game["lines"], MEDIUM_FONT, CYAN, PANEL_X, 315)


    draw_text("Difficulty", FONT, WHITE, PANEL_X, 355)
    draw_text(game["difficulty"], FONT, ORANGE, PANEL_X, 380)


    draw_text("Line Stats", FONT, WHITE, PANEL_X, 415)
    draw_text("Single: " + str(game["stats"]["single"]),
              FONT, WHITE, PANEL_X, 440)
    draw_text("Double: " + str(game["stats"]["double"]),
              FONT, WHITE, PANEL_X, 462)
    draw_text("Triple: " + str(game["stats"]["triple"]),
              FONT, WHITE, PANEL_X, 484)
    draw_text("Tetris: " + str(game["stats"]["tetris"]),
              FONT, WHITE, PANEL_X, 506)


    if game["combo"] > 0:
        draw_text("Combo: " + str(game["combo"]),
                  FONT, GREEN, PANEL_X, 535)


    if game["back_to_back"]:
        draw_text("Back-to-Back!", FONT, YELLOW, PANEL_X, 558)


    pygame.display.flip()


def draw_start_menu():
    screen.fill(BLACK)


    draw_text("TETRIS", TITLE_FONT, CYAN,
              SCREEN_WIDTH // 2, 90, True)


    draw_centered_lines([
        "Choose Difficulty",
        "1 - Easy",
        "2 - Normal",
        "3 - Hard",
        "",
        "Press a number to start",
        "Arrow keys: Move",
        "Up arrow: Rotate",
        "Down arrow: Soft drop",
        "Space: Hard drop",
        "P: Pause"
    ], FONT, WHITE, 175, 32)


    pygame.display.flip()


def draw_leaderboard():
    screen.fill(BLACK)


    draw_text("GAME OVER", TITLE_FONT, RED,
              SCREEN_WIDTH // 2, 60, True)
    draw_text("TOP 5 SCORES", MEDIUM_FONT, YELLOW,
              SCREEN_WIDTH // 2, 140, True)


    if not leaderboard:
        draw_text("No scores yet", FONT, WHITE,
                  SCREEN_WIDTH // 2, 190, True)


    for index, entry in enumerate(leaderboard):
        line = (
            str(index + 1) + ". " +
            str(entry["score"]) + "  " +
            entry["difficulty"] + "  Level " +
            str(entry["level"])
        )
        draw_text(line, FONT, WHITE, 60, 195 + index * 35)


    draw_centered_lines([
        "Press ENTER to play again",
        "Press M for menu",
        "Press ESC to quit"
    ], FONT, CYAN, 420, 35)


    pygame.display.flip()


def main():
    state = "menu"
    game = None
    running = True
    paused = False
    difficulty = "Normal"
    soft_drop_held = False


    while running:
        dt = clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    soft_drop_held = False


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


                elif state == "menu":
                    if event.key == pygame.K_1:
                        difficulty = "Easy"
                        game = create_game(difficulty)
                        state = "playing"
                    elif event.key == pygame.K_2:
                        difficulty = "Normal"
                        game = create_game(difficulty)
                        state = "playing"
                    elif event.key == pygame.K_3:
                        difficulty = "Hard"
                        game = create_game(difficulty)
                        state = "playing"


                elif state == "playing":
                    if event.key == pygame.K_LEFT:
                        move_piece(game, -1, 0)
                    elif event.key == pygame.K_RIGHT:
                        move_piece(game, 1, 0)
                    elif event.key == pygame.K_UP:
                        rotate_piece(game)
                    elif event.key == pygame.K_SPACE:
                        if not hard_drop(game):
                            finish_game(game)
                            state = "gameover"
                    elif event.key == pygame.K_DOWN:
                        soft_drop_held = True
                        if move_piece(game, 0, 1):
                            update_score(game, 1)
                        else:
                            if not lock_piece(game):
                                finish_game(game)
                                state = "gameover"
                    elif event.key == pygame.K_p:
                        paused = not paused


                elif state == "gameover":
                    if event.key == pygame.K_RETURN:
                        game = create_game(difficulty)
                        state = "playing"
                        paused = False
                    elif event.key == pygame.K_m:
                        state = "menu"
                        paused = False


        if state == "menu":
            draw_start_menu()


        elif state == "playing":
            if not paused:
                game["fall_timer"] += dt


                if soft_drop_held:
                    game["soft_timer"] += dt
                    if game["soft_timer"] >= 50:
                        game["soft_timer"] = 0
                        if move_piece(game, 0, 1):
                            update_score(game, 1)
                        else:
                            if not lock_piece(game):
                                finish_game(game)
                                state = "gameover"
                else:
                    game["soft_timer"] = 0


                if game["fall_timer"] >= get_fall_speed(game):
                    game["fall_timer"] = 0


                    if not move_piece(game, 0, 1):
                        if not lock_piece(game):
                            finish_game(game)
                            state = "gameover"


            if state == "playing":
                draw_board(game)


                if paused:
                    overlay = pygame.Surface(
                        (SCREEN_WIDTH, SCREEN_HEIGHT),
                        pygame.SRCALPHA
                    )
                    overlay.fill((0, 0, 0, 180))
                    screen.blit(overlay, (0, 0))
                    draw_text("PAUSED", TITLE_FONT, WHITE,
                              SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, True)
                    draw_text("Press P to continue", FONT, WHITE,
                              SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, True)
                    pygame.display.flip()


        elif state == "gameover":
            draw_leaderboard()


    pygame.quit()


if __name__ == "__main__":
    main()
