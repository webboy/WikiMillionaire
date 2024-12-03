from data_models.player import Player


class PlayerService:
    """
    Service class for managing players in the game.
    """

    def __init__(self):
        """
        Initialize the PlayerService with an empty player list.
        """
        self.players = []

    def add_player(self, username: str) -> Player:
        """
        Add a new player to the service.
        :param username: The username of the player to add.
        :return: The Player instance that was added.
        """
        # Validate and create a Player instance
        player = Player(username=username)

        # Check if the username already exists
        if any(p.username == player.username for p in self.players):
            raise ValueError(f"Player with username '{username}' already exists.")

        # Add to the list of players
        self.players.append(player)
        return player

    def find_player_by_username(self, username: str) -> Player:
        """
        Find a player by their username.
        :param username: The username to search for.
        :return: The Player instance if found.
        :raises ValueError: If the player does not exist.
        """
        for player in self.players:
            if player.username == username:
                return player
        raise ValueError(f"Player with username '{username}' not found.")

    def remove_player_by_username(self, username: str) -> bool:
        """
        Remove a player by their username.
        :param username: The username of the player to remove.
        :return: True if the player was removed, False otherwise.
        """
        for player in self.players:
            if player.username == username:
                self.players.remove(player)
                return True
        return False

    def list_players(self) -> list:
        """
        List all players in the service.
        :return: A list of Player instances.
        """
        return self.players
