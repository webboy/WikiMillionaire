import json


class Question:
    """
    A class representing a multiple-choice trivia question.
    """

    def __init__(self, question: str, options: dict, correct_answer: str, source: str, hint: str = "", difficulty: int = 50):
        """
        Initialize the Question instance.
        :param question: The question text.
        :param options: A dictionary of answer options (e.g., {"A": "Option 1", "B": "Option 2"}).
        :param correct_answer: The correct answer as a letter (e.g., "A").
        :param source: The source URL of the question.
        :param hint: A hint to help the user answer the question.
        :param difficulty: An integer between 1 and 100 indicating difficulty level.
        """
        if len(options) > 6:
            raise ValueError("Options cannot exceed 6 possible answers.")
        if correct_answer not in options:
            raise ValueError("Correct answer must be one of the provided options.")
        if not (1 <= difficulty <= 100):
            raise ValueError("Difficulty must be between 1 and 100.")

        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.source = source
        self.hint = hint
        self.difficulty = difficulty

    def is_correct(self, answer: str) -> bool:
        """
        Check if the given answer is correct.
        :param answer: The answer to check (e.g., "A").
        :return: True if the answer is correct, otherwise False.
        """
        return answer.upper() == self.correct_answer

    def format(self) -> str:
        """
        Format the question and its options for display.
        :return: A formatted string representing the question and options.
        """
        output = f"{self.question}\n"
        for letter, option in self.options.items():
            output += f"{letter}. {option}\n"
        return output

    def shuffle_options(self):
        """
        Shuffle the options and update the correct answer accordingly.
        """
        import random

        # Convert options into a list of (letter, option) pairs
        options_list = list(self.options.items())

        # Find the correct option before shuffling
        correct_option = self.options[self.correct_answer]

        # Shuffle the options
        random.shuffle(options_list)

        # Update the options and correct answer
        self.options = {chr(65 + i): option for i, (_, option) in enumerate(options_list)}
        for letter, option in self.options.items():
            if option == correct_option:
                self.correct_answer = letter
                break

    def to_dict(self) -> dict:
        """
        Convert the Question instance to a dictionary.
        :return: A dictionary representation of the Question instance.
        """
        return {
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "source": self.source,
            "hint": self.hint,
            "difficulty": self.difficulty
        }

    def to_json(self) -> str:
        """
        Convert the Question instance to a JSON string.
        :return: A JSON string representation of the Question instance.
        """
        return json.dumps(self.to_dict(), indent=4)

    @staticmethod
    def from_dict(data: dict):
        """
        Create a Question instance from a dictionary.
        :param data: A dictionary containing the question data.
        :return: A Question instance.
        """
        return Question(
            question=data["question"],
            options=data["options"],
            correct_answer=data["correct_answer"],
            source=data.get("source", "wikipedia"),
            hint=data.get("hint", ""),  # Default to an empty hint if not provided
            difficulty=data.get("difficulty", 50)  # Default difficulty to 50 if not provided
        )

    @staticmethod
    def from_json(json_str: str):
        """
        Create a Question instance from a JSON string.
        :param json_str: A JSON string containing the question data.
        :return: A Question instance.
        """
        data = json.loads(json_str)
        return Question.from_dict(data)
