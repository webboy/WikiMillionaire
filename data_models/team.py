from data_models.player import Player


class Team:
    """
    A class representing a team in the game.
    """

    def __init__(self, name: str, max_players: int):
        """
        Initialize the Team instance.
        :param name: The team's name.
        :param max_players: Maximum number of players allowed in the team.
        """
        if not name or not name.strip():
            raise ValueError("Team name cannot be empty.")
        if len(name.strip()) < 3:
            raise ValueError("Team name must be at least 3 characters long.")

        self.name = name.strip()
        self.max_players = max_players
        self.players = []

    def add_player(self, player: Player):
        """
        Add a player to the team.
        :param player: A Player instance to add.
        """
        if len(self.players) >= self.max_players:
            raise ValueError(f"Team '{self.name}' cannot have more than {self.max_players} players.")
        if player in self.players:
            raise ValueError(f"Player '{player.username}' is already in the team.")
        self.players.append(player)

    def remove_player(self, username: str):
        """
        Remove a player by username.
        :param username: The username of the player to remove.
        """
        self.players = [p for p in self.players if p.username != username]

    def list_players(self):
        """
        List all players in the team.
        :return: A list of Player instances.
        """
        return self.players

    def to_dict(self) -> dict:
        """
        Convert the Team instance to a dictionary.
        :return: A dictionary representation of the Team instance.
        """
        return {
            "name": self.name,
            "max_players": self.max_players,
            "players": [player.to_dict() for player in self.players]
        }
