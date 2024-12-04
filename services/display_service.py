import os
import time

# Function to center the text in terminal window
class DisplayService:
    def __init__(self):
        self.GOLD = "\033[33m"  # Yellow text color (for the title)
        self.GREEN = "\033[32m"  # Green text color (for the messages)
        self.RESET = "\033[0m"  # Reset color code to return to default terminal colors

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
        ready_message = f"{self.GREEN}Are you ready to become a Millionaire? Let's get started!{self.RESET}"

        # The new rules introduction message
        rules_message = f"""{self.GREEN}  
    But first, let us introduce you to the rules:
    1. You need to answer each question by typing the letter displayed before each option.
    2. You have limited amount of time to answer each question.
    3. You can use available jokers to help you out.
    4. You must answer all questions correctly to become the MILLIONAIRE.
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