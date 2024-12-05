import os
import time

from data_models.team import Team


# Function to center the text in terminal window
class DisplayService:
    def __init__(self):
        self.GOLD = "\033[33m"  # Yellow text color (for the title)
        self.GREEN = "\033[32m"  # Green text color (for the messages)
        self.RESET = "\033[0m"  # Reset color code to return to default terminal colors
        self.BLUE = "\033[0;34m"  # blue
        self.RED = "\033[31m"  # Red text color

    # Function to center the text in terminal window
    def __center_text(self, text, width=80):
        lines = text.split("\n")  # split input text into lines based on newlines
        centered_lines = [line.center(width) for line in lines]  # centering each line based on width
        return "\n".join(centered_lines)  # centered lines joined back into a single string

    # Function to print text line by line with a delay
    def __print_text_line_by_line(self, text, delay=0.1):
        """Function to print text line by line with a delay"""
        for line in text.split('\n'):
            print(line)
            time.sleep(delay)

    # Function to display welcome screen
    def print_welcome_screen(self):
        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')  # clears screen with 'cls' on windows and with 'clear' for Unix systems like OS on mac or LINUX

        # ASCII Art for "Wikimillionaire"
        welcome_art = f""" {self.GOLD}   
             ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗              
             ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗            
             ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗         ██║   ██║   ██║            
             ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝         ██║   ██║   ██║            
             ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝            
              ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝             
      ██╗    ██╗██╗██╗  ██╗██╗███╗   ███╗██╗██╗     ██╗     ██╗ ██████╗ ███╗   ██╗ █████╗ ██╗██████╗ ███████╗ 
      ██║    ██║██║██║ ██╔╝██║████╗ ████║██║██║     ██║     ██║██╔═══██╗████╗  ██║██╔══██╗██║██╔══██╗██╔════╝ 
      ██║ █╗ ██║██║█████╔╝ ██║██╔████╔██║██║██║     ██║     ██║██║   ██║██╔██╗ ██║███████║██║██████╔╝█████╗   
      ██║███╗██║██║██╔═██╗ ██║██║╚██╔╝██║██║██║     ██║     ██║██║   ██║██║╚██╗██║██╔══██║██║██╔══██╗██╔══╝   
      ╚███╔███╔╝██║██║  ██╗██║██║ ╚═╝ ██║██║███████╗███████╗██║╚██████╔╝██║ ╚████║██║  ██║██║██║  ██║███████╗ 
       ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝ 
    {self.RESET}
        """

        # Calculate the width of the welcome ASCII art (based on the longest line)
        ascii_art_lines = welcome_art.split("\n")
        ascii_art_width = max(len(line) for line in ascii_art_lines)

        # Center the welcome ASCII art
        centered_art = self.__center_text(welcome_art, ascii_art_width)

        # Print the centered ASCII art line by line with a delay
        self.__print_text_line_by_line(centered_art, delay=0.2)

        # Define green text messages for the welcome screen
        welcome_message = f"{self.GREEN}Welcome to Wikimillionaire Game!{self.RESET}"
        test_message = f"{self.GREEN}Prepare to test your knowledge and teamwork skills to beat the game!{self.RESET}"
        ready_message = f"{self.GREEN}Are you ready to become a {self.__millionaire()}{self.GREEN}? Let's get started!{self.RESET}"

        # The new rules introduction message
        rules_message = f"""{self.GREEN}  
    But first, let us introduce you to the rules:
    1. You need to answer each question by typing the letter displayed before each option.
    2. You have limited amount of time to answer each question.
    3. You can use available jokers to help you out.
    4. You must answer all questions correctly to become the {self.__millionaire()}{self.GREEN}.
    5. You can reach safety levels which guarantee the secured amount.
    6. You can type 'quit' to quit the game and take home the amount you secured throughout the game.
    {self.RESET}"""

        good_luck_message = f"{self.GREEN}Good Luck and Have Fun!{self.RESET}"

        # Strip leading/trailing spaces and center each message relative to the previous message
        centered_welcome_message = self.__center_text(welcome_message.strip(), ascii_art_width)
        previous_message_width = len(centered_welcome_message.split('\n')[0])  # Width of the first message

        # Center all the following messages relative to the previous message's width
        centered_test_message = self.__center_text(test_message.strip(), previous_message_width)
        previous_message_width = len(centered_test_message.split('\n')[0])  # Update width for the next message

        centered_ready_message = self.__center_text(ready_message.strip(), previous_message_width)
        previous_message_width = len(centered_ready_message.split('\n')[0])  # Update width for the next message

        centered_rules_message = self.__center_text(rules_message.strip(), previous_message_width)
        previous_message_width = len(centered_rules_message.split('\n')[0])  # Update width for the next message

        centered_good_luck_message = self.__center_text(good_luck_message.strip(), previous_message_width)

        # Print each welcome message line by line with a delay
        self.__print_text_line_by_line(centered_welcome_message, delay=0.03)
        self.__print_text_line_by_line(centered_test_message, delay=0.03)
        self.__print_text_line_by_line(centered_ready_message, delay=0.3)
        time.sleep(2)  # Pause after the ready message

        # Print the rules message line by line with a delay
        self.__print_text_line_by_line(centered_rules_message, delay=0.3)

        # Print the final good luck message
        self.__print_text_line_by_line(centered_good_luck_message, delay=0.1)

        # Wait for 2 seconds before moving on, allowing the user to read the welcome screen
        time.sleep(2)

    def print_end_screen(self):
        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')  # clears screen

        print(f"Meh..... ok, it looks like you really are a {self.__millionaire()} material, but....")

        # ASCII Art for "Game Over"
        end_art = f""" {self.GOLD}  
  ██████╗  ██████╗     ███╗   ██╗ ██████╗ ████████╗    ███████╗ ██████╗ ██████╗  ██████╗ ███████╗████████╗
  ██╔══██╗██╔═══██╗    ████╗  ██║██╔═══██╗╚══██╔══╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝
  ██║  ██║██║   ██║    ██╔██╗ ██║██║   ██║   ██║       █████╗  ██║   ██║██████╔╝██║  ███╗█████╗     ██║   
  ██║  ██║██║   ██║    ██║╚██╗██║██║   ██║   ██║       ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝     ██║   
  ██████╔╝╚██████╔╝    ██║ ╚████║╚██████╔╝   ██║       ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗   ██║   
  ╚═════╝  ╚═════╝     ╚═╝  ╚═══╝ ╚═════╝    ╚═╝       ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
  ████████╗ ██████╗     ██████╗  █████╗ ██╗   ██╗    ████████╗ █████╗ ██╗  ██╗███████╗███████╗       ██╗  
  ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗╚██╗ ██╔╝    ╚══██╔══╝██╔══██╗╚██╗██╔╝██╔════╝██╔════╝    ██╗╚██╗ 
     ██║   ██║   ██║    ██████╔╝███████║ ╚████╔╝        ██║   ███████║ ╚███╔╝ █████╗  ███████╗    ╚═╝ ██║ 
     ██║   ██║   ██║    ██╔═══╝ ██╔══██║  ╚██╔╝         ██║   ██╔══██║ ██╔██╗ ██╔══╝  ╚════██║    ▄█╗ ██║ 
     ██║   ╚██████╔╝    ██║     ██║  ██║   ██║          ██║   ██║  ██║██╔╝ ██╗███████╗███████║    ▀═╝██╔╝ 
     ╚═╝    ╚═════╝     ╚═╝     ╚═╝  ╚═╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝       ╚═╝  
   {self.RESET}
       """

        # Calculate the width of the end ASCII art
        ascii_art_lines = end_art.split("\n")
        ascii_art_width = max(len(line) for line in ascii_art_lines)

        # Center the end ASCII art
        centered_end_art = self.__center_text(end_art, ascii_art_width)

        # Print the centered ASCII art line by line with a delay
        self.__print_text_line_by_line(centered_end_art, delay=0.2)

        # Define green text messages for the end screen
        thank_you_message = f"{self.GREEN}Thank you for playing!{self.RESET}"
        final_message = f"{self.GREEN}We hope you had fun and learned something new!{self.RESET}"

        # Strip leading/trailing spaces and center each message relative to the previous message
        centered_thank_you_message = self.__center_text(thank_you_message.strip(), ascii_art_width)
        previous_message_width = len(centered_thank_you_message.split('\n')[0])  # Width of the first message

        centered_final_message = self.__center_text(final_message.strip(), previous_message_width)

        # Print each end message line by line with a delay
        self.__print_text_line_by_line(centered_thank_you_message, delay=0.03)
        self.__print_text_line_by_line(centered_final_message, delay=0.1)

        # Wait for 2 seconds before exiting
        time.sleep(2)

    def display_difficulties(self, difficulties):
        for key, difficulty in difficulties.items():
            print(f"\n {difficulty.identifier.upper()} :")
            print(f"Number of questions: {len(difficulty.prizes)}")
            print(f"Number of options: {difficulty.options_number}")
            print(f"Time to answer: {difficulty.question_time}")

    def line_break(self):
        print(f"{self.GOLD}{'=' * 100}{self.RESET}")

    def display_team_welcome(self, team: Team) -> None:
        print(f"Ok, it's time to see if you have what it takes to become {self.__millionaire()}")
        print(f"Go, Go {self.BLUE}{team.name}{self.RESET}!")

    def display_time_attention(self, time_remaining):
        print(f"\n{self.RED}Attention{self.RESET}: You have {self.RED}{time_remaining:.2f}{self.RESET} seconds to answer the question.")

    def display_question_header(self, current_player, index, prizes, prize):
        print(f"Get ready {self.GREEN}{current_player.username}{self.RESET}, it's time to answer the question!")
        print(f"Question {index + 1} / {len(prizes)} for ${prize}:\n")

    def time_up(self, time_limit):
        print(f"\n{self.RED}Timed out after {time_limit} seconds, sorry. Press [ENTER] to continue...{self.RESET}")

    def display_wrong_answer(self, current_player, question, answer):
        print(f"{self.RED}Uh, oh..... Wrong answer, {self.GREEN}{current_player.username}{self.RED}!{self.RESET}")
        print(f"The correct answer is '{question.correct_answer}' and you answered with '{answer}'.")
        print(f"Come on, now, did you really think you can become a {self.__millionaire()}? You did? Ok then, try again.")

    def display_correct_answer(self, current_player, prize, game):
        print(f"Correct! {self.GREEN}{current_player.username}{self.RESET} has won {self.GOLD}${prize}{self.RESET}"
              f" for the {self.BLUE}{game.team.name}{self.RESET} team!")

    def __millionaire(self):
        return f"{self.GOLD}MILLIONAIRE{self.RESET}"
