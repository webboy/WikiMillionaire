# Import packages
import os
import time
import threading
from dotenv import load_dotenv
# Import data models
from data_models.difficulty import Difficulty
from data_models.team import Team
from data_models.question import Question
from data_models.game import Game
# Import services
from services.openai_service import OpenAIService
from services.wikipedia_service import WikipediaService
from services.difficulty_service import DifficultyService
from services.display_service import DisplayService
from services.user_input_service import UserInputService
from services.sound_service import SoundService
# Import widgets
from widgets.spinner_widget import SpinnerWidget


def ask_question(game, wikipedia_service, openai_service, sound_service, display_service, spinner, wiki_max_tries, openai_max_tries):
    """
    Handles the logic for asking a single question in the game with a 30-second timer.

    :param sound_service: SoundService instance
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
    time_limit = game.difficulty.question_time

    display_service.line_break()

    display_service.display_question_header(current_player, index, prizes, prize)

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

    def timer_thread(timeout_event, duration):
        """
        Timer thread that counts down and sets the timeout_event when time runs out.
        """
        for remaining in range(duration, 0, -1):
            if timeout_event.is_set():  # Stop the timer if timeout_event is already set
                return
            time.sleep(1)
        timeout_event.set()  # Trigger timeout_event when time runs out

    def print_question_thread(d_question: Question):

        nonlocal answer_event
        nonlocal timeout_event
        nonlocal answer_container
        nonlocal display_service

        # Calculate remaining time
        remaining_time = time_limit - (time.time() - start_time)

        # Display the question and options
        print(d_question.format())

        # Extract available options dynamically
        available_options = ", ".join(d_question.options.keys())

        # Get the player's answer
        display_service.display_time_attention(remaining_time)

        # jokers
        available_jokers = game.jokers.keys()
        if available_jokers:
            print(f"\nYou have {len(available_jokers)} jokers. Type the following commands to use the joker:")
            for joker_index in available_jokers:
                print(f"{joker_index} - {game.jokers[joker_index].name}")
        else:
            print(f"\nYou have no available jokers.")

        user_answer = input(f"\nYour answer ({available_options}):").strip()

        if user_answer in available_jokers:
            d_question = game.jokers[user_answer].apply(d_question)
            print(f"You have just used the joker: {game.jokers[user_answer].name}.")
            del (game.jokers[user_answer])
            print_question_thread(d_question)
        else:
            answer_container["answer"] = user_answer  # Store the answer in a shared container
            answer_event.set()

    start_time = time.time()

    # Shared container and events for threads
    answer_event = threading.Event()
    timeout_event = threading.Event()
    answer_container = {}

    # Start threads
    ask_thread = threading.Thread(
        target=print_question_thread,
        args=(question,),
        daemon=True,
    )
    timer_thread = threading.Thread(
        target=timer_thread,
        args=(timeout_event, time_limit),
        daemon=True,
    )

    ask_thread.start()
    timer_thread.start()

    # Wait for either event to be triggered
    while not (answer_event.is_set() or timeout_event.is_set()):
        time.sleep(0.1)  # Avoid busy-waiting

    safe_prize = max(
        [p for level, p in safe_levels.items() if int(level) <= int(index + 1)],
        default=0,
    )
    if answer_event.is_set():
        timeout_event.set()  # Stop the timer thread

        answer = answer_container.get("answer", "")
        # Validate the answer
        if answer == 'quit':
            print(
                f"We are sorry to see you leaving, {current_player.username}, but we understand life is not always about playing games.")
            print(f"Your team leaves with ${safe_prize}.")
            ask_thread.join()
            timer_thread.join()
            return False, safe_prize

        if question.is_correct(answer):
            display_service.line_break()
            display_service.display_correct_answer(current_player, prize, game)
            game.add_question(question)
            ask_thread.join()
            timer_thread.join()
            sound_service.play_answer_sound()
            return True, prize

        # Handle incorrect answer
        sound_service.play_answer_sound()
        display_service.display_wrong_answer(current_player, question, answer)

        print(f"Your team leaves with ${safe_prize}.")
        ask_thread.join()
        timer_thread.join()
        return False, safe_prize

    if timeout_event.is_set():
        display_service.time_up(time_limit)

        ask_thread.join()
        timer_thread.join()
        return False, safe_prize


def setup_team(user_input_service: UserInputService) -> Team:
    """
    Set up a team at the start of the game.
    :return: A Team instance.
    """

    max_players = int(os.getenv("MAX_TEAM_PLAYERS", 4))

    # Create the team
    default_team_name = str(os.getenv("DEFAULT_TEAM_NAME", "PentaBytes"))
    while True:
        try:
            team_name = user_input_service.input_for_team_name(default_team_name)
            #input(f"Enter your team name (default: {default_team_name}): ").strip()
            if not team_name:
                team_name = default_team_name  # Use default name if none is provided
            team = Team(name=team_name, max_players=max_players)
            break
        except ValueError as e:
            print(f"Error: {e}")

    num_players = user_input_service.input_for_players_number(max_players)

    default_username_prefix = str(os.getenv("DEFAULT_USERNAME", "Player"))
    for i in range(num_players):
        player = user_input_service.input_for_single_player_name(i, default_username_prefix)
        team.add_player(player)

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


def choose_difficulty(
        difficulty_service: DifficultyService,
        user_input_service: UserInputService,
        display_service: DisplayService
) -> Difficulty:
    """
    Let the player choose a difficulty level and return the corresponding Difficulty object.
    """
    difficulty_service.load_difficulties()
    available_difficulties = difficulty_service.list_difficulties()

    print(f"It's time to choose a difficulty level. Be careful now...")

    default_difficulty = str(os.getenv("DEFAULT_DIFFICULTY", "easy"))

    display_service.display_difficulties(difficulty_service.difficulties)

    selected_difficulty = user_input_service.input_for_difficulty_level(available_difficulties, default_difficulty)

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
        user_input_service = UserInputService()
        sound_service = SoundService()

        # Initialize widgets
        spinner = SpinnerWidget()

        # Display welcome screen
        sound_service.play_opening_sound()
        display_service.print_welcome_screen()

        # Set up the team
        team = setup_team(user_input_service)

        display_service.line_break()

        # Choose difficulty
        difficulty = choose_difficulty(difficulty_service, user_input_service, display_service)
        display_service.line_break()

        # Initialize the game
        game = Game(team, difficulty)

        display_service.display_team_welcome(game.team)

        # Game loop
        while game.current_question_index < len(game.difficulty.prizes):
            is_correct, prize_or_safe_prize = ask_question(
                game,
                wikipedia_service,
                openai_service,
                sound_service,
                display_service,
                spinner,
                wiki_max_tries,
                openai_max_tries
            )
            if is_correct:
                if game.current_question_index == len(game.difficulty.prizes) - 1:
                    # The team became MILLIONAIRE
                    game.win_game(prize_or_safe_prize)
                    sound_service.play_end_sound()
                    display_service.print_end_screen()
            else:
                game.finish_game(prize_or_safe_prize)
                break
            # Mark the current question as completed and update indexes
            game.update_player_index()
            game.update_question_index()

        # Display the game duration
        print(f"You answered {len(game.questions)} questions correctly.")
        print(f"Your game lasted for {str(game.get_time_elapsed()).split('.')[0]} seconds.")

        display_service.line_break()

        # Ask if the user wants to play again
        while True:
            play_again = input("\nDo you want to play again? (Y/n): ").strip().lower()
            if play_again == "n":
                print("Thank you for playing Wiki Millionaire! Goodbye!")
                quit()
            if play_again == "y":
                break
            print(f"Did you said '{play_again}'? Come on, you know better than that.")


if __name__ == "__main__":
    main()
