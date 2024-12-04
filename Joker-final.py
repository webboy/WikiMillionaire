import time
import threading
import random

def apply_fifty_fifty(question, options):
  incorrect_options = [option for option in options if option != question['correct_answer']]
  random.shuffle(incorrect_options)

  # Calculate the number of incorrect options to remove (half, rounded up)
  num_to_remove = len(incorrect_options) // 2 + 1

  options_to_remove = incorrect_options[:num_to_remove]

  for option_to_remove in options_to_remove:
      options.pop(option_to_remove)

  return question, options

def loading_bar(duration):
    RED = '\033[91m'
    ENDCOLOR = '\033[0m'
    paused = False
    start_time = time.time()

    while duration > 0:
        if not paused:
            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_time = duration - int(elapsed_time)

            if remaining_time <= 0:
                break

            filled_length = int(remaining_time / duration * 10)
            print(f"\r{RED}[{filled_length * '='}{(10 - filled_length) * ' '}] {remaining_time}s remaining{ENDCOLOR}", end="")
            time.sleep(1)  # Adjust sleep time as needed for smoother display
        else:
            print("\rTimer paused. Press 'r' to resume.", end="")

        # Check for user input to pause/resume
        user_input = input()
        if user_input == 'p':
            paused = True
        elif user_input == 'r':
            paused = False
            start_time = time.time()  # Reset the start time

    print("\nTime's up!")

def run_timer(timer_duration):
    loading_bar(timer_duration)
    print("\nTime's up!")  # Prints "Time's up!" when the timer expires

def main():
    question = {
        "question": "What is the capital of France?",
        "options": {
            "A": "Paris",
            "B": "London",
            "C": "Berlin",
            "D": "Madrid",
            "E": "Rome",
            "F": "Tokyo"
        },
        "correct_answer": "A"
    }

    joker_used = False
    timer_duration = 30

    def create_and_start_timer():
        """Creates and starts a timer thread."""

        timer_thread = threading.Thread(target=run_timer, args=(timer_duration,))
        timer_thread.start()
        return timer_thread

    timer_thread = create_and_start_timer()  # Start the timer thread

    print(question['question'])
    for letter, option in question['options'].items():
        print(f"{letter}. {option}")

    while True:
        user_input = input("Enter your answer (A-F) or 'use joker': ")

        if user_input.lower() == "use joker" and not joker_used:
            question, options = apply_fifty_fifty(question, question['options'])
            joker_used = True
            timer_duration += 15  # Extend the timer
            print("Joker activated! Two incorrect options removed and the timer gains 15sec.")
            print(question['question'])
            for letter, option in question['options'].items():
                print(f"{letter}. {option}")
            # Reset the timer after joker usage
            timer_thread.join()  # Stop the previous timer thread
            timer_thread = create_and_start_timer()  # Create and start a new timer

        elif user_input in question['options']:
            timer_thread.join()  # Stop the timer
            break
        else:
            print("Invalid input. Please enter a valid letter or 'use joker'.")


if __name__ == "__main__":
    main()