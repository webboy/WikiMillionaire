class User_Input:
    def __init__(self):
        self.inputs = []


    def input_validation(self, user_answers): #players answer
        valid_inputs = ['A', 'B', 'C', 'D', 'E', 'F', 'END', 'hint', '50/50']
        while True:
            user_answer_input = input(f"Please choose your answer {user_answers}: ").upper().strip()
            if user_answer_input in valid_inputs:
                return user_answer_input
            print("Invalid input! Please choose a valid option.")


    def single_player_name(self):
        player_names = []
        for i in range(num_players):
            name = input(f"Enter the name of player {i + 1}: ")
            player_names.append(name)


    def team_name(self):
        while True:
            team_name_string = input("Please enter your team name: ").strip().upper()
            if len(team_name_string) >= 10:
                return team_name_string
            else:
                print("Team name must be at least 5 characters long.")


    def amount_group_of_players(self, players):
        if isinstance(players, (int, list)):
            num_players = len(players) if isinstance(players, list) else players
            if 2 <= num_players <= 10:
                return f"There are {num_players} players."
            else:
                return "Invalid number of players. The number must be between 1 and 10."
        else:
            return "Invalid input. Please provide an integer or a list."


    def difficulty_level(self):
        while True:
            chosen_difficulty_level = input("Please choose difficulty (easy, medium, hard): ").lower().strip()
            if chosen_difficulty_level in ['easy', 'medium', 'hard']:
                return chosen_difficulty_level
            else:
                print("Invalid input! Please Try again.")


    def choice_of_extra_joker(self):
        while True:
            choice = input("Do you want to play in safety mode or risk mode? (safety/risk): ").lower().strip()
            if choice in ['safety', 'risk']:
                return choice
            else:
                print("Invalid input! Please enter 'safety' or 'risk'.")