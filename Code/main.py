from core.game_engine import GameEngine


def main() -> None:
    """Application entry point for Team Yellow Tetris."""
    engine = GameEngine(
        width=800,
        height=600,
        title="Team Yellow Tetris",
        target_fps=60
    )
    engine.run()


if __name__ == "__main__":
    main()