import threading
import time
import sys
import select

def ask_question(question, answer_event, timeout_event, answer_container):
    """
    Simulate asking the user a question with a custom input that respects timeout.
    """
    print(question.format())  # Display the question
    print("\nEnter your answer (A, B, C, D, E, F): ", end="", flush=True)

    # Wait for input while respecting the timeout
    while not timeout_event.is_set():
        if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:  # Check for input
            answer = sys.stdin.readline().strip().upper()
            if not timeout_event.is_set():  # Only process if timer hasn't expired
                answer_container["answer"] = answer
                answer_event.set()
            return
    # If timeout_event is set, simply return
    print("\nNo input registered before timeout.")


def start_timer(timeout_event, duration):
    """
    Run a countdown timer and set timeout_event if time expires.
    """
    for remaining in range(duration, 0, -1):
        if timeout_event.is_set():  # Stop the timer if timeout_event is already set
            return
        print(f"\rTime remaining: {remaining} seconds", end="", flush=True)
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

        # Create threads for the question and timer (non-daemon)
        ask_thread = threading.Thread(
            target=ask_question,
            args=(question, answer_event, timeout_event, answer_container),
        )
        timer_thread = threading.Thread(
            target=start_timer,
            args=(timeout_event, duration),
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
