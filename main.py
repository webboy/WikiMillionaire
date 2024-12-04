import os
import time
import threading
from dotenv import load_dotenv
from data_models.player import Player
from data_models.difficulty import Difficulty
from data_models.team import Team
from data_models.question import Question
from data_models.game import Game
from services.openai_service import OpenAIService
from services.wikipedia_service import WikipediaService
from services.difficulty_service import DifficultyService
from services.display_service import DisplayService
from widgets.spinner_widget import SpinnerWidget

def ask_question(game, wikipedia_service, openai_service, spinner, wiki_max_tries, openai_max_tries, time_limit = 30):
    """
    Handles the logic for asking a single question in the game with a 30-second timer.

    :param time_limit: Time limit in seconds for the answer
    :param game: The current Game instance.
    :param wikipedia_service: WikipediaService instance.
    :param openai_service: OpenAIService instance.
    :param spinner: SpinnerWidget instance for user feedback.
    :param wiki_max_tries: Maximum attempts for fetching Wikipedia summaries.
    :param openai_max_tries: Maximum attempts for generating questions.
    :return: Tuple (is_correct, safe_prize) indicating whether the question was answered correctly
             and the prize to award in case of incorrect answers.
    """
    current_player = game.get_current_player()
    prizes = game.difficulty.prizes
    difficulty = game.difficulty
    safe_levels = game.difficulty.safe_levels
    index = game.current_question_index
    prize = prizes[index]



    print(f"It's {current_player.username}'s turn!")
    print(f"\nQuestion {index + 1} / {len(prizes)} for ${prize}:")

    # Get random Wikipedia summary with retries
    summary = fetch_random_wikipedia_summary(wikipedia_service, wiki_max_tries, spinner)

    # Generate a question using OpenAI with retries
    question = generate_question_from_openai(
        openai_service,
        text=summary,
        source="Wikipedia",
        max_attempts=openai_max_tries,
        spinner=spinner,
    )

    # Prepare the question
    question = prepare_question(question, difficulty)

    def print_question(d_question: Question):

        # Calculate remaining time
        remaining_time = time_limit - (time.time() - start_time)

        # Display the question and options
        print(d_question.format())

        # Extract available options dynamically
        available_options = ", ".join(d_question.options.keys())

        # Get the player's answer
        print(f"\n Attention: You have {remaining_time:.2f} seconds to answer the question.")

        # jokers
        available_jokers = game.jokers.keys()
        if available_jokers:
            print(f"\nYou have {len(available_jokers)} jokers. Type the following commands to use the joker:")
            for joker_index in available_jokers:
                print(f"\n{joker_index} - {game.jokers[joker_index].name}")
        else:
            print(f"\nYou have no available jokers.")

        answer = input(f"\nYour answer ({available_options}):").strip()

        if answer in available_jokers:
            d_question = game.jokers[answer].apply(d_question)
            print(f"You have just used the joker: {game.jokers[answer].name}.")
            del (game.jokers[answer])
            return print_question(d_question)

        return answer

    start_time = time.time()

    answer = print_question(question)

    elapsed_time = time.time() - start_time

    safe_prize = max(
        [p for level, p in safe_levels.items() if int(level) <= int(index + 1)],
        default=0,
    )

    if elapsed_time > time_limit:
        print(f"\nYou took {elapsed_time:.2f} seconds to answer the question. That's over the limit of {time_limit} seconds. Sorry.")
        return False, safe_prize

    # Validate the answer
    if question.is_correct(answer):
        print(f"Correct! {current_player.username} has won ${prize} for the {game.team.name} team!")
        game.add_question(question)
        return True, prize

    # Handle incorrect answer
    print(f"Wrong answer, {current_player.username}!")
    print(f"The correct answer is '{question.correct_answer}' and you answered with '{answer}'.")


    print(f"Your team leaves with ${safe_prize}.")
    return False, safe_prize

def setup_team() -> Team:
    """
    Set up a team at the start of the game.
    :return: A Team instance.
    """

    max_players = int(os.getenv("MAX_TEAM_PLAYERS", 4))

    # Create the team
    default_team_name = str(os.getenv("DEFAULT_TEAM_NAME", "PentaBytes"))
    while True:
        try:
            team_name = input(f"Enter your team name (default: {default_team_name}): ").strip()
            if not team_name:
                team_name = default_team_name  # Use default name if none is provided
            team = Team(name=team_name, max_players=max_players)
            break
        except ValueError as e:
            print(f"Error: {e}")

    # Add players to the team
    while True:
        try:
            user_input = input(f"Enter the number of players in your team (1-{max_players}), default is 1: ").strip()
            if not user_input:  # If input is empty, use the default value
                num_players = 1
            else:
                num_players = int(user_input)
            if num_players < 1 or num_players > max_players:
                raise ValueError
            break
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {max_players}.")

    default_username_prefix = str(os.getenv("DEFAULT_USERNAME", "Player"))
    for _ in range(num_players):
        while True:
            try:
                default_username = f"{default_username_prefix} {str(_ + 1)}"
                username = input(f"Enter the username for the player (default: {default_username}): ").strip()
                if not username:
                    username = default_username
                player = Player(username=username)
                team.add_player(player)
                break
            except ValueError as e:
                print(f"Error: {e}")

    return team

def prepare_question(question, difficulty) -> Question:
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
        selected_difficulty = input("Choose a difficulty (easy, medium, hard), default is easy: ").strip().lower()
        if not selected_difficulty:
            selected_difficulty = "easy"

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

def generate_question_from_openai(openai_service, text, source, max_attempts, spinner) -> Question:
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
    while True:  # Infinite loop to replay the game
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

        # Display welcome screen
        display_service.print_welcome_screen("Player") #todo: Welcome screen no longer needs username, update the method.

        # Set up the team
        team = setup_team()

        # Choose difficulty
        difficulty = choose_difficulty(difficulty_service)

        # Initialize the game
        game = Game(team, difficulty)

        prizes = game.difficulty.prizes
        safe_levels = game.difficulty.safe_levels

        # Game loop
        while game.current_question_index < len(game.difficulty.prizes):

            is_correct, prize_or_safe_prize = ask_question(
                game,
                wikipedia_service,
                openai_service,
                spinner,
                wiki_max_tries,
                openai_max_tries,
                20


            )
            if is_correct:
                if game.current_question_index == len(game.difficulty.prizes) - 1:
                    game.win_game(prize_or_safe_prize)
                    print(f"You won. Your team is now millionaires")
            else:
                game.finish_game(prize_or_safe_prize)
                break
            # Mark the current question as completed and update indexes
            game.update_player_index()
            game.update_question_index()

        # Display the game duration
        print(f"You answered {game.current_question_index + 1} questions.")
        print(f"Your game lasted for {str(game.get_time_elapsed()).split('.')[0]} seconds.")

        # Ask if the user wants to play again
        play_again = input("\nDo you want to play again? (Y/n): ").strip().lower()
        if play_again == "n":
            print("Thank you for playing Wiki Millionaire! Goodbye!")
            break


if __name__ == "__main__":
    main()
