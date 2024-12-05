import json
from data_models.difficulty import Difficulty
import os
import sys


class DifficultyService:
    """
    Service class to handle difficulty levels.
    """

    def __init__(self, file_path: str = "data/difficulties.json"):
        """
        Initialize the DifficultyService with the file path for difficulties.
        :param file_path: Path to the JSON file containing difficulty settings.
        """
        self.file_path = self.get_resource_path(file_path)
        self.difficulties = {}

    def get_resource_path(self, relative_path):
        """Get the absolute path to a resource in a PyInstaller bundle."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def load_difficulties(self):
        """
        Load difficulties from the JSON file into the service.
        """
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.difficulties = {
                    key: Difficulty.from_dict(value) for key, value in data.items()
                }
        except FileNotFoundError:
            raise FileNotFoundError(f"Difficulty file not found at {self.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {self.file_path}")

    def get_difficulty(self, identifier: str) -> Difficulty:
        """
        Get a Difficulty instance by its identifier.
        :param identifier: The identifier of the difficulty level (e.g., 'easy').
        :return: A Difficulty instance.
        """
        if identifier in self.difficulties:
            return self.difficulties[identifier]
        raise ValueError(f"Difficulty with identifier '{identifier}' not found.")

    def list_difficulties(self) -> list:
        """
        Return a list of available difficulty identifiers.
        :return: A list of difficulty identifiers (e.g., ['easy', 'medium', 'hard']).
        """
        return list(self.difficulties.keys())
