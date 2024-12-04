import time
import threading

class TriviaGame:
    def __init__(self, question, correct_answer, time_limit):
        self.question = question
        self.correct_answer = correct_answer
        self.time_limit = time_limit
        self.time_remaining = time_limit
        self.timer_thread = None

    # Timer function
    def countdown_timer(self):
        start_time = time.time()
        while self.time_remaining > 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self.time_remaining = self.time_limit - elapsed_time
            if self.time_remaining <= 0:
                print("\nTime's up!")
                break

    # Function to start the trivia game
    def start_game(self):
        # Start the timer in a separate thread
        self.timer_thread = threading.Thread(target=self.countdown_timer)
        self.timer_thread.start()

        # Ask the user the question within the time limit
        while self.time_remaining > 0:
            user_answer = input(f"\n{self.question} You have ({int(self.time_remaining)}s remaining) > ")
            if user_answer.lower() == self.correct_answer.lower():
                print("Correct!")
                break
            else:
                print("Wrong answer! Try again.")
            time.sleep(0.1)  # Small delay to prevent tight loops

        if self.time_remaining <= 0:
            print("Time's up! You didn't answer in time.")

# Example usage:
game = TriviaGame("What is the capital of France?", "Paris", 10)
game.start_game()