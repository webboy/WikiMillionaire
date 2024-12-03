class Difficulty:
    """
    Represents the difficulty level in the game.
    """

    def __init__(self, identifier: str, prizes: list, safe_levels: dict, options_number: int):
        """
        Initialize a Difficulty instance.
        :param identifier: The difficulty identifier (e.g., 'easy', 'medium', 'hard').
        :param prizes: A list of prize amounts.
        :param safe_levels: A dictionary mapping question numbers to guaranteed prize amounts.
        :param options_number: Number of options per question (e.g., 3, 4, 6).
        """
        self.identifier = identifier
        self.prizes = prizes
        self.safe_levels = safe_levels
        self.options_number = options_number

    def to_dict(self) -> dict:
        """
        Convert the Difficulty instance to a dictionary.
        :return: A dictionary representation of the Difficulty instance.
        """
        return {
            "identifier": self.identifier,
            "prizes": self.prizes,
            "safe_levels": self.safe_levels,
            "options_number": self.options_number,
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Create a Difficulty instance from a dictionary.
        :param data: A dictionary containing the difficulty data.
        :return: A Difficulty instance.
        """
        return Difficulty(
            identifier=data["identifier"],
            prizes=data["prizes"],
            safe_levels=data["safe_levels"],
            options_number=data["options_number"],
        )
