import os
from dotenv import load_dotenv
from data_models.player import Player
from data_models.difficulty import Difficulty
from services.openai_service import OpenAIService
from services.wikipedia_service import WikipediaService
from services.difficulty_service import DifficultyService
from services.display_service import DisplayService
from widgets.spinner_widget import SpinnerWidget

def prepare_question(question, difficulty):
    """
    Modify the Question object to include only the number of options allowed by the difficulty.
    Ensures the correct answer is retained in the final options.

    :param question: The Question object to prepare.
    :param difficulty: The Difficulty object specifying the number of options.
    :return: The modified Question object.
    """
    num_options = difficulty.options_number
    correct_option = question.correct_answer

    # Retain the correct answer and reduce options to fit the difficulty level
    if correct_option not in question.options:
        raise ValueError("The correct answer is not in the question options.")

    final_options = {}

    # Add other options until the required number is reached
    for key, value in question.options.items():
        if len(final_options) >= num_options:
            break
        final_options[key] = value

    # Update the Question object's options without reassigning keys
    question.options = final_options

    return question

def choose_difficulty(difficulty_service) -> Difficulty :
    """
    Let the player choose a difficulty level and return the corresponding Difficulty object.
    """
    difficulty_service.load_difficulties()
    available_difficulties = difficulty_service.list_difficulties()
    print("\nAvailable difficulties:", ", ".join(available_difficulties))

    selected_difficulty = None
    while selected_difficulty not in available_difficulties:
        selected_difficulty = input("Choose a difficulty (easy, medium, hard): ").strip().lower()

    return difficulty_service.get_difficulty(selected_difficulty)


def fetch_random_wikipedia_summary(wikipedia_service, max_attempts, spinner):
    """
    Fetch a random Wikipedia summary with retries and spinner feedback.
    """
    for attempt in range(1, max_attempts + 1):
        spinner.start(f" Attempt {attempt}: Fetching text from Wikipedia...")
        summary = wikipedia_service.get_random_summary()
        spinner.stop()
        if "Error" not in summary:
            return summary
        print(f"\nAttempt {attempt} to fetch Wikipedia summary failed.")
    spinner.stop()
    print("\nFailed to fetch a random Wikipedia page after multiple attempts.")
    quit()


def generate_question_from_openai(openai_service, text, source, max_attempts, spinner):
    """
    Generate a question from OpenAI with retries and spinner feedback.
    """
    for attempt in range(1, max_attempts + 1):
        spinner.start(f" Attempt {attempt}: Generating question from OpenAI...")
        question = openai_service.get_question_from_text(text=text, source=source)
        spinner.stop()
        if not isinstance(question, dict) or "error" not in question:
            return question
        print(f"\nAttempt {attempt} to generate a question failed: {question['error']}")
    spinner.stop()
    print("\nFailed to generate a question from OpenAI after multiple attempts.")
    quit()


def main():
    # Load environment variables
    load_dotenv()
    wiki_max_tries = int(os.getenv("WIKI_MAX_TRIES", 3))
    openai_max_tries = int(os.getenv("OPENAI_MAX_TRIES", 3))

    # Initialize services
    wikipedia_service = WikipediaService()
    openai_service = OpenAIService()
    difficulty_service = DifficultyService()
    display_service = DisplayService()

    # Initialize widgets
    spinner = SpinnerWidget()

    # Create a dummy player
    player = Player(username="Player1")
    display_service.print_welcome_screen(player.username)

    # Choose difficulty
    difficulty = choose_difficulty(difficulty_service)
    prizes = difficulty.prizes
    safe_levels = difficulty.safe_levels

    # Game loop
    for index, prize in enumerate(prizes, start=1):
        print(f"\nQuestion {index} / {len(prizes)} for ${prize}:")

        # Get random Wikipedia summary with retries
        summary = fetch_random_wikipedia_summary(wikipedia_service, wiki_max_tries, spinner)

        # Generate a question using OpenAI with retries
        question = generate_question_from_openai(openai_service, text=summary, source="Wikipedia",
                                                 max_attempts=openai_max_tries, spinner=spinner)

        # Prepare teh question
        question = prepare_question(question, difficulty)
        # Display the question and options
        print(question.format())
        answer = input("Your answer (A, B, C, D, E, F): ").strip().upper()

        # Validate the answer
        if question.is_correct(answer):
            print(f"Correct! You've won ${prize}!")
            if prize == prizes[-1]:
                print("Congratulations! You are a millionaire!")
                break
        else:
            print("Wrong answer!")
            safe_prize = max([p for level, p in safe_levels.items() if int(level) <= int(index)], default=0)
            print(f"You leave with ${safe_prize}.")
            break


if __name__ == "__main__":
    main()
