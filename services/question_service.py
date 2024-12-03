from data_models.question import Question
import json
import random

class QuestionService:
    """
    Service class for handling Question-related operations.
    """

    def __init__(self):
        self.questions = []

    def add_question(self, question: Question):
        self.questions.append(question)

    def get_random_question(self) -> Question:
        if not self.questions:
            raise ValueError("No questions available.")
        return random.choice(self.questions)

    def load_questions_from_json(self, json_file: str):
        with open(json_file, 'r') as file:
            data = json.load(file)
            for q in data:
                self.questions.append(Question.from_dict(q))

    def save_questions_to_json(self, json_file: str):
        with open(json_file, 'w') as file:
            json.dump([q.to_dict() for q in self.questions], file, indent=4)

    def find_question_by_text(self, text: str) -> Question:
        for question in self.questions:
            if question.question == text:
                return question
        raise ValueError("Question not found.")

    def find_question_by_difficulty_range(self, min_difficulty: int, max_difficulty: int):
        if not (1 <= min_difficulty <= 100 and 1 <= max_difficulty <= 100):
            raise ValueError("Difficulty range must be between 1 and 100.")
        if min_difficulty > max_difficulty:
            raise ValueError("Minimum difficulty cannot be greater than maximum difficulty.")

        return [
            question for question in self.questions
            if min_difficulty <= question.difficulty <= max_difficulty
        ]

    def get_random_question_by_difficulty_range(self, min_difficulty: int, max_difficulty: int) -> Question:
        filtered_questions = self.find_question_by_difficulty_range(min_difficulty, max_difficulty)
        if not filtered_questions:
            raise ValueError(f"No questions found within difficulty range {min_difficulty}-{max_difficulty}.")
        return random.choice(filtered_questions)
