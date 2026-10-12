import pytest
from domain.high_score_repository import FileHighScoreRepository


@pytest.fixture
def repo(tmp_path):
    # Saves to a temporary folder, so the real score file is never touched
    return FileHighScoreRepository(str(tmp_path / "scores.json"))


def test_missing_file_gives_no_scores(repo):
    assert repo.load_scores() == []
    assert repo.load_high_score() == 0


def test_scores_are_saved_best_first(repo):
    repo.add_score(300)
    repo.add_score(900)
    repo.add_score(100)
    assert repo.load_scores() == [900, 300, 100]


def test_only_the_top_five_are_kept(repo):
    for score in [100, 200, 300, 400, 500, 600, 700]:
        repo.add_score(score)
    assert repo.load_scores() == [700, 600, 500, 400, 300]


def test_corrupt_file_gives_no_scores(tmp_path):
    bad_file = tmp_path / "scores.json"
    bad_file.write_text("not json")
    assert FileHighScoreRepository(str(bad_file)).load_scores() == []


def test_high_score_is_the_best_saved(repo):
    repo.add_score(300)
    repo.add_score(900)
    assert repo.load_high_score() == 900
