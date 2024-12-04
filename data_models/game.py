from datetime import datetime, timedelta
from enum import Enum
from data_models.team import Team
from data_models.difficulty import Difficulty


class GameStatus(Enum):
    ONGOING = "ongoing"
    FINISHED = "finished"  # User made a wrong answer
    WON = "won"            # Team answered the final question
    INTERRUPTED = "interrupted"  # An error occurred


class Game:
    """
    Represents the state of a game.
    """

    def __init__(self, team: Team, difficulty: Difficulty):
        """
        Initialize a new Game instance.
        :param team: The Team object participating in the game.
        :param difficulty: The Difficulty object for the game.
        """
        self.time_started = datetime.now()
        self.time_finished = None
        self.team = team
        self.difficulty = difficulty
        self.current_question_index = 0
        self.current_player_index = 0
        self.status = GameStatus.ONGOING
        self.amount_won = 0

    def update_question_index(self):
        """
        Increment the current question index.
        """
        if self.current_question_index < len(self.difficulty.prizes) - 1:
            self.current_question_index += 1
        else:
            self.win_game()

    def update_player_index(self):
        """
        Increment the current player index in a round-robin fashion.
        """
        self.current_player_index = (self.current_player_index + 1) % len(self.team.players)

    def finish_game(self, amount_won = 0, wrong_answer=True):
        """
        Mark the game as finished or interrupted.
        :param amount_won: Amount won at the end of the game
        :param wrong_answer: If True, the game ended due to a wrong answer. Otherwise, it was interrupted.
        """
        self.time_finished = datetime.now()
        self.status = GameStatus.FINISHED if wrong_answer else GameStatus.INTERRUPTED
        self.amount_won = int(amount_won)

    def win_game(self, amount_won = 0):
        """
        Mark the game as won.
        """
        self.time_finished = datetime.now()
        self.status = GameStatus.WON
        self.amount_won = int(amount_won)

    def get_progress(self):
        """
        Get the game progress as a percentage.
        :return: Progress as a float between 0 and 1.
        """
        return self.current_question_index / len(self.difficulty.prizes)

    def get_current_player(self):
        """
        Retrieves the current player from the team based on the current
        player's index.

        :return: The player instance that is currently active.
        """
        return self.team.players[self.current_player_index]

    def get_time_elapsed(self) -> timedelta:
        """
        Calculate the time elapsed from the game's start to its finish,
        or to the current time if the game is ongoing.

        :return: A timedelta object representing the elapsed time.
        """
        end_time = self.time_finished if self.time_finished else datetime.now()
        return end_time - self.time_started

    def to_dict(self):
        """
        Serialize the game object to a dictionary.
        """
        return {
            "time_started": self.time_started.isoformat(),
            "time_finished": self.time_finished.isoformat() if self.time_finished else None,
            "team": self.team.to_dict(),
            "difficulty": self.difficulty.to_dict(),
            "current_question_index": self.current_question_index,
            "current_player_index": self.current_player_index,
            "status": self.status.value,
        }
