from data_models.difficulty import Difficulty


def test_difficulty_initialization():
    difficulty = Difficulty(
        identifier="medium",
        prizes=[100, 200, 300],
        safe_levels={1: 100, 2: 200},
        options_number=4,
    )

    assert difficulty.identifier == "medium"
    assert difficulty.prizes == [100, 200, 300]
    assert difficulty.safe_levels == {1: 100, 2: 200}
    assert difficulty.options_number == 4


def test_difficulty_to_dict():
    difficulty = Difficulty(
        identifier="easy",
        prizes=[100, 1000, 10000],
        safe_levels={2: 1000, 3: 10000},
        options_number=3,
    )
    expected_dict = {
        "identifier": "easy",
        "prizes": [100, 1000, 10000],
        "safe_levels": {2: 1000, 3: 10000},
        "options_number": 3,
    }
    assert difficulty.to_dict() == expected_dict


def test_difficulty_from_dict():
    data = {
        "identifier": "hard",
        "prizes": [100, 200, 300],
        "safe_levels": {1: 100, 2: 200},
        "options_number": 6,
    }
    difficulty = Difficulty.from_dict(data)

    assert difficulty.identifier == "hard"
    assert difficulty.prizes == [100, 200, 300]
    assert difficulty.safe_levels == {1: 100, 2: 200}
    assert difficulty.options_number == 6
