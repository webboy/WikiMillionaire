class Player:
    """
    A class representing a player in the game.
    """

    def __init__(self, username: str):
        """
        Initialize the Player instance.
        :param username: The player's username.
        """
        if not username or not username.strip():
            raise ValueError("Username cannot be empty.")
        if len(username.strip()) < 1:
            raise ValueError("Username must be at least 5 characters long.")
        self.username = username.strip()

    def to_dict(self) -> dict:
        """
        Convert the Player instance to a dictionary.
        :return: A dictionary representation of the Player instance.
        """
        return {
            "username": self.username
        }

    def to_json(self) -> str:
        """
        Convert the Player instance to a JSON string.
        :return: A JSON string representation of the Player instance.
        """
        import json
        return json.dumps(self.to_dict(), indent=4)

    @staticmethod
    def from_dict(data: dict):
        """
        Create a Player instance from a dictionary.
        :param data: A dictionary containing the player data.
        :return: A Player instance.
        """
        return Player(username=data["username"])

    @staticmethod
    def from_json(json_str: str):
        """
        Create a Player instance from a JSON string.
        :param json_str: A JSON string containing the player data.
        :return: A Player instance.
        """
        import json
        data = json.loads(json_str)
        return Player.from_dict(data)
