import os
import pytest

from chess.controllers.player_controller import PlayerController


def test_player_creation():
    pc = PlayerController()
    assert pc is not None


TEST_FILE = "data/test_players.json"


class PlayerControllerForTest(PlayerController):
    FILE_PATH = TEST_FILE


@pytest.fixture(autouse=True)
def cleanup():
    os.makedirs("data", exist_ok=True)
    """Removes the test file before and after each test."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_add_new_player():
    pc = PlayerControllerForTest()
    assert pc.add_player("Alice") is True
    assert "Alice" in pc.list_players()


def test_add_duplicate_player():
    pc = PlayerControllerForTest()
    pc.add_player("Alice")
    assert pc.add_player("Alice") is False
