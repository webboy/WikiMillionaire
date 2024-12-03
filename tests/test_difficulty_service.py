import pytest
from services.difficulty_service import DifficultyService
from data_models.difficulty import Difficulty
import json


@pytest.fixture
def mock_difficulty_file(tmp_path):
    # Create a temporary JSON file with difficulty data
    difficulties = {
        "easy": {
            "identifier": "easy",
            "prizes": [100, 1000, 10000],
            "safe_levels": {"2": 1000, "3": 10000},
            "options_number": 3,
        },
        "medium": {
            "identifier": "medium",
            "prizes": [100, 200, 300],
            "safe_levels": {"2": 200, "3": 300},
            "options_number": 4,
        },
    }
    file_path = tmp_path / "difficulties.json"
    with open(file_path, "w") as f:
        json.dump(difficulties, f)
    return file_path


def test_load_difficulties(mock_difficulty_file):
    service = DifficultyService(file_path=str(mock_difficulty_file))
    service.load_difficulties()

    assert len(service.difficulties) == 2
    assert isinstance(service.difficulties["easy"], Difficulty)
    assert isinstance(service.difficulties["medium"], Difficulty)


def test_get_difficulty(mock_difficulty_file):
    service = DifficultyService(file_path=str(mock_difficulty_file))
    service.load_difficulties()

    easy = service.get_difficulty("easy")
    assert easy.identifier == "easy"
    assert easy.prizes == [100, 1000, 10000]
    assert easy.safe_levels == {'2': 1000, '3': 10000}
    assert easy.options_number == 3

    with pytest.raises(ValueError, match="Difficulty with identifier 'hard' not found."):
        service.get_difficulty("hard")


def test_list_difficulties(mock_difficulty_file):
    service = DifficultyService(file_path=str(mock_difficulty_file))
    service.load_difficulties()

    difficulties = service.list_difficulties()
    assert difficulties == ["easy", "medium"]
