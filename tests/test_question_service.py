from services.question_service import QuestionService
from data_models.question import Question
import pytest


@pytest.fixture
def service_with_questions():
    service = QuestionService()
    service.add_question(Question(
        question="What is the capital of France?",
        options={"A": "Paris", "B": "London", "C": "Berlin", "D": "Rome"},
        correct_answer="A",
        source="https://example.com",
        difficulty=30
    ))
    service.add_question(Question(
        question="When was Python created?",
        options={"A": "1991", "B": "1989"},
        correct_answer="A",
        source="https://example.com",
        difficulty=50
    ))
    return service


def test_add_question(service_with_questions):
    service = service_with_questions
    assert len(service.questions) == 2


def test_find_question_by_difficulty_range(service_with_questions):
    service = service_with_questions
    results = service.find_question_by_difficulty_range(10, 40)
    assert len(results) == 1
    assert results[0].question == "What is the capital of France?"
