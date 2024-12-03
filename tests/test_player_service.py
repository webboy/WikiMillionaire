import pytest
from services.player_service import PlayerService

@pytest.fixture
def player_service():
    return PlayerService()


def test_add_player(player_service):
    player = player_service.add_player("ValidUser")
    assert player.username == "ValidUser"
    assert len(player_service.players) == 1


def test_add_duplicate_player(player_service):
    player_service.add_player("ValidUser")
    with pytest.raises(ValueError, match="Player with username 'ValidUser' already exists."):
        player_service.add_player("ValidUser")


def test_find_player_by_username(player_service):
    player_service.add_player("ValidUser")
    player = player_service.find_player_by_username("ValidUser")
    assert player.username == "ValidUser"


def test_find_player_by_username_not_found(player_service):
    with pytest.raises(ValueError, match="Player with username 'NonExistent' not found."):
        player_service.find_player_by_username("NonExistent")


def test_remove_player_by_username(player_service):
    player_service.add_player("ValidUser")
    assert player_service.remove_player_by_username("ValidUser") is True
    assert len(player_service.players) == 0


def test_remove_player_by_username_not_found(player_service):
    assert player_service.remove_player_by_username("NonExistent") is False


def test_list_players(player_service):
    player_service.add_player("User1")
    player_service.add_player("User2")
    players = player_service.list_players()
    assert len(players) == 2
    assert players[0].username == "User1"
    assert players[1].username == "User2"
