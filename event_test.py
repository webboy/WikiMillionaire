import threading
import time

def ask_question(question, answer_event, timeout_event, answer_container):
    """
    Simulate asking the user a question.
    """
    print(question.format())  # Display the question
    print("\nEnter your answer (A, B, C, D, E, F): ", end="", flush=True)

    # Wait for the user's input while the timeout thread is running
    answer = input().strip().upper()

    if not timeout_event.is_set():  # Only set answer_event if the timer hasn't expired
        answer_container["answer"] = answer  # Store the answer in a shared container
        answer_event.set()


def start_timer(timeout_event, duration):
    """
    Run a countdown timer and set timeout_event if time expires.
    """
    for remaining in range(duration, 0, -1):
        if timeout_event.is_set():  # Stop the timer if timeout_event is already set
            return
        # print(f"\rTime remaining: {remaining} seconds", end="", flush=True)
        time.sleep(1)
    timeout_event.set()  # Trigger timeout_event when time runs out
    print("\nTime's up!")


def game_loop():
    """
    Main game loop.
    """
    # Example question object
    question = type('Question', (object,), {})()  # Mock Question object
    question.format = lambda: "What is the capital of France?\nA. Paris\nB. London\nC. Berlin\nD. Madrid"

    duration = 10  # Timer duration in seconds
    while True:
        # Create threading events
        answer_event = threading.Event()
        timeout_event = threading.Event()

        # Shared container for the user's answer
        answer_container = {}

        # Create threads for the question and timer
        ask_thread = threading.Thread(
            target=ask_question,
            args=(question, answer_event, timeout_event, answer_container),
            daemon=True
        )
        timer_thread = threading.Thread(
            target=start_timer,
            args=(timeout_event, duration),
            daemon=True
        )

        # Start the threads
        ask_thread.start()
        timer_thread.start()

        # Wait for either event
        while not (answer_event.is_set() or timeout_event.is_set()):
            time.sleep(0.1)  # Polling delay to avoid busy-waiting

        # Handle the event that was triggered
        if answer_event.is_set():
            # Stop the timer
            timeout_event.set()

            # Get the user's answer
            user_answer = answer_container.get("answer", "")
            print(f"\nYou answered: {user_answer}")

            # Process the answer (for now, assume game continues)
            if user_answer == "A":
                print("Correct! The game continues.")
            else:
                print("Wrong answer. Game over!")
                break
        elif timeout_event.is_set():
            # Stop the ask thread
            answer_event.set()
            print("\nTime's up! Game over!")
            break

        # Ensure threads are stopped before starting new ones
        ask_thread.join()
        timer_thread.join()

        # Continue to the next question
        print("\nNext question...\n")


if __name__ == "__main__":
    game_loop()
