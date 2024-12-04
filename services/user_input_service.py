import os

from data_models.player import Player


class UserInputService:
    def __init__(self):
        # ANSI codes for colors to be used in the text
        self.GOLD = "\033[33m"  # Yellow text color (for the title)
        self.GREEN = "\033[32m"  # Green text color (for right answers)
        self.YELLOW = "\033[0;33m" # Yellow text color (for player name)
        self.RED = "\033[31m"# Red text color (for Error messages)
        self.RESET = "\033[0m"  # Reset color code to return to default terminal colors
        self.BLUE = "\033[0;34m"#blue

        self.minimum_username_length = os.getenv('MINIMUM_USERNAME_LENGTH', 3)
        self.minimum_team_name_length = os.getenv('MINIMUM_TEAM_NAME_LENGTH', 3)

    def input_for_question_answer(self): #players answer
        valid_inputs = ['A', 'B', 'C', 'D', 'E', 'F', 'HINT', '50/50']
        end_input = "END"
        while True:
            user_answer_input = input(f"Please choose your answer: ").upper().strip()
            if user_answer_input in valid_inputs:
                return f"{self.GREEN}{user_answer_input}{self.RESET}"
            elif user_answer_input in end_input:
                return f"{self.RED}{end_input}{self.RESET}"
            print(f"{self.RED}Invalid input! Please choose a valid option.{self.RESET}")


    def input_for_single_player_name(self, player_number, default_username_prefix):
        while True:
            default_username = f"{default_username_prefix} {str(player_number + 1)}"
            username = input(f"Enter the username for the player (default: {default_username}): ").strip()
            if not username:
                username = default_username
            if len(username) >= self.minimum_username_length:
                player = Player(username=username)
                return player
            print(f"{self.RED}Team name must be at least {self.minimum_username_length} characters long.{self.RESET}")


    def input_for_team_name(self, default_team_name):
        while True:
            team_name_string = input(f"Enter your team name (default: {default_team_name}): ").strip()
            if not team_name_string:
                team_name_string = default_team_name
            if len(team_name_string) >= self.minimum_team_name_length:
                return team_name_string
            else:
                print(f"{self.RED}Team name must be at least {self.minimum_team_name_length} characters long.{self.RESET}")

    def input_for_players_number(self, max_players) -> int:
        while True:
            try:
                user_input = input(
                    f"Enter the number of players in your team (1-{max_players}), default is 1: ").strip()
                if not user_input:  # If input is empty, use the default value
                    num_players = 1
                else:
                    num_players = int(user_input)
                if num_players < 1 or num_players > max_players:
                    raise ValueError
                break
            except ValueError:
                print(f"{self.RED}Invalid input. Please enter a number between 1 and {max_players}.{self.RESET}")

        return num_players

    def input_for_difficulty_level(self, available_difficulty_levels, default_difficulty):
        while True:
            chosen_difficulty_level = input(f"Please choose difficulty ({", ".join(available_difficulty_levels)}) default is {default_difficulty}: ").lower().strip()

            if not chosen_difficulty_level:
                chosen_difficulty_level = default_difficulty

            if chosen_difficulty_level in available_difficulty_levels:
                return chosen_difficulty_level
            else:
                print(f"{self.RED}Invalid input! Please Try again.{self.RESET}")


    def choice_of_extra_joker(self):
        while True:
                choice = input("Do you want to play in 'safety' mode or 'risk' mode? (safety/risk): ").lower().strip()
                if choice in ['safety', 'risk']:
                    return choice 
                else:
                    print(f"{self.RED}Invalid input! Please enter either 'safety' or 'risk'.{self.RESET}")