#import the module to interact with operating system,e.g clear the screen
import os
#time module to introduce delays for redeability
import time


#function to center the text in terminal window, I hate this step btw haha
def center_text(text, width=80):
    lines = text.split("\n") #split input text into lines based on newlines
    centered_lines = [line.center(width) for line in lines] #centering each line based on width
    return "\n".join(centered_lines) #centered lines joined back into a single string

#Function to display welcome
def print_welcome_screen():
    #clear the termonal
    os.system('cls' if os.name == 'nt' else 'clear') #clears screen with 'cls' on windows and with 'clear' for Unix systems like OS on mac or LINUX

    # ANSI codes for colors to be used in the text, you can look it up online they are basically rgb codes for colors
    GOLD = "\033[33m"  # Yellow text color (for the title)
    GREEN = "\033[32m"  # Green text color (for the messages)
    '''BLUE 
       PURPLE
       WHITE''' #same logic can be used to assign colors to players/teams

    RESET = "\033[0m"  # Reset color code to return to default terminal colors

    # ASCII Art for "Wikimillionaire"
    welcome_art = f""" {GOLD}   
           ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗            
'          ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗           
'          ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗         ██║   ██║   ██║           
'          ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝         ██║   ██║   ██║           
'          ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝           
'           ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝            
'  ██╗    ██╗██╗██╗  ██╗██╗███╗   ███╗██╗██╗     ██╗     ██╗ ██████╗ ███╗   ██╗ █████╗ ██╗██████╗ ███████╗
'  ██║    ██║██║██║ ██╔╝██║████╗ ████║██║██║     ██║     ██║██╔═══██╗████╗  ██║██╔══██╗██║██╔══██╗██╔════╝
'  ██║ █╗ ██║██║█████╔╝ ██║██╔████╔██║██║██║     ██║     ██║██║   ██║██╔██╗ ██║███████║██║██████╔╝█████╗  
'  ██║███╗██║██║██╔═██╗ ██║██║╚██╔╝██║██║██║     ██║     ██║██║   ██║██║╚██╗██║██╔══██║██║██╔══██╗██╔══╝  
'  ╚███╔███╔╝██║██║  ██╗██║██║ ╚═╝ ██║██║███████╗███████╗██║╚██████╔╝██║ ╚████║██║  ██║██║██║  ██║███████╗
'   ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
{RESET}
    """

    # Set the terminal width, defaulting to 80 characters if os.get_terminal_size() is unavailable
    terminal_width = 80  # This can be dynamically fetched, but we're using a fixed value here

    # Center the welcome ASCII art
    centered_art = center_text(welcome_art, terminal_width)

    # Print the centered ASCII art to the terminal
    print(centered_art)

    # Define green text messages for the welcome screen
    welcome_message = f"{GREEN}Welcome to Wikimillionaire Game!{RESET}"
    test_message = f"{GREEN}Prepare to test your knowledge and teamwork skills to beat the game!{RESET}"
    ready_message = f"{GREEN}Are you ready to become a Millionaire? Let's get started!{RESET}"

    # The new rules introduction message
    rules_message = f"""{GREEN}
    But first, let us introduce you to the rules:
    Players get to choose their team names.
    Each team gets 3 lives against the game.
    You are competing not only with the game, but also with time.
    But do not worry, you get 3 jokers to help you win:
    1. Hint 2. Pass it on  3. Skip
    {RESET}
        """

    goodluck_message = f"{GREEN} Good Luck and Have Fun!{RESET}"

    # Center each of the green messages within the terminal width
    centered_welcome_message = center_text(welcome_message, terminal_width)
    centered_test_message = center_text(test_message, terminal_width)
    centered_ready_message = center_text(ready_message, terminal_width)
    #centered_rules_message = center_text(rules_message, terminal_width)
    centered_goodluck_message = center_text(goodluck_message, terminal_width)

    # Print the centered green text messages to the terminal
    print(centered_welcome_message)
    print(centered_test_message)
    print(centered_ready_message)

    print(rules_message)  # Print the rules message
    print(centered_goodluck_message)

    # Wait for 2 seconds before moving on, allowing the user to read the welcome screen
    time.sleep(2)

        # Ask for user input (simple prompt)
    user_name = input(f"{GREEN}Enter your team name to continue: {RESET}")
    print(f"\nHello,{GOLD} {user_name} {RESET}! Let's begin the game!\n")


# Main function to start the game
def main():
    print_welcome_screen()  # Display the welcome screen when the game starts


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()  # Start the game by calling the main function