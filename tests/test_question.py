from data_models.question import Question
import pytest


def test_question_initialization():
    question = Question(
        question="What is the capital of France?",
        options={"A": "Paris", "B": "London", "C": "Berlin", "D": "Rome"},
        correct_answer="A",
        source="https://example.com",
        hint="It’s known as the City of Light.",
        difficulty=30
    )

    assert question.question == "What is the capital of France?"
    assert question.correct_answer == "A"
    assert question.hint == "It’s known as the City of Light."
    assert question.difficulty == 30


def test_question_is_correct():
    question = Question(
        question="What is the capital of France?",
        options={"A": "Paris", "B": "London", "C": "Berlin", "D": "Rome"},
        correct_answer="A",
        source="https://example.com",
        difficulty=30
    )

    assert question.is_correct("A")
    assert question.is_correct("a")  # Case-insensitive
    assert not question.is_correct("B")


def test_question_invalid_difficulty():
    with pytest.raises(ValueError):
        Question(
            question="Invalid question",
            options={"A": "Yes", "B": "No"},
            correct_answer="A",
            source="https://example.com",
            difficulty=200  # Out of range
        )
