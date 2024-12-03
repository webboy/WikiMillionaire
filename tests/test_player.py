import pytest
from data_models.player import Player


def test_player_initialization():
    player = Player(username="ValidUser")
    assert player.username == "ValidUser"


def test_player_invalid_username_empty():
    with pytest.raises(ValueError, match="Username cannot be empty."):
        Player(username=" ")


def test_player_invalid_username_too_short():
    with pytest.raises(ValueError, match="Username must be at least 5 characters long."):
        Player(username="User")


def test_player_to_dict():
    player = Player(username="ValidUser")
    expected_dict = {"username": "ValidUser"}
    assert player.to_dict() == expected_dict


def test_player_to_json():
    player = Player(username="ValidUser")
    expected_json = '{\n    "username": "ValidUser"\n}'
    assert player.to_json() == expected_json


def test_player_from_dict():
    data = {"username": "ValidUser"}
    player = Player.from_dict(data)
    assert player.username == "ValidUser"


def test_player_from_json():
    json_str = '{"username": "ValidUser"}'
    player = Player.from_json(json_str)
    assert player.username == "ValidUser"
