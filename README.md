# 🧠 Wiki Millionaire

**Wiki Millionaire** is a trivia game inspired by the popular TV show *Who Wants to Be a Millionaire?*. The game dynamically generates questions using **Wikipedia** and **OpenAI**, allowing players or teams to compete by answering questions of varying difficulty levels.

---

## 🎮 Features

- **Dynamic Question Generation**: Questions are generated using Wikipedia summaries and processed with OpenAI for diverse and challenging trivia.
- **Team Play**: Supports team-based gameplay with customizable team sizes.
- **Difficulty Levels**: Players can choose from *Easy*, *Medium*, or *Hard* modes, affecting the number of options, prizes, and questions.
- **Real-Time Timer**: Adds urgency with a countdown timer for each question.
- **Sound Effects and Music**: Background music and sound effects enhance the gameplay experience.

---

## 📂 Project Structure

```plaintext
.
├── data_models/            # Data models for Question, Player, Team, etc.
├── services/               # Service classes for handling game logic, sound, and external APIs.
├── data/                   # JSON files for difficulty settings and other game data.
├── media/                  # Folder containing sound files (background music, effects).
├── tests/                  # Unit tests for various components of the game.
├── widgets/                # Reusable terminal widgets like the spinner.
├── main.py                 # Entry point of the game.
└── README.md               # Project documentation (this file).
```

## 🚀 🚀 Getting Started
### Prerequisites
Python 3.8+

Install required packages:
```bash
pip install -r requirements.txt
```
Media Files: Ensure that the media/ folder contains the following files:

```
answer_sound.mp3
end_sound.mp3
opening_sound.mp3
background_sound.mp3
```
## How to Play
Run the Game:

```bash
python main.py
```
Choose a Difficulty: Select from Easy, Medium, or Hard modes.

Answer Questions: Questions are dynamically generated. Enter the correct option (A-F) within the allotted time.

Play Again: After the game ends, choose whether to start a new game or exit.

## 🛠 Programming features
- Usage of classes
- Multi-threading (Implementation of the countdown timer)
- Usage of Wikipedia API
- Usage of OpenAI API
- Usage of sound (``` pygame```) package
- Reading from ```.env``` file
- Data storage using JSON files

## 📋 Future Enhancements
Leaderboard: Track high scores across multiple sessions.
Hints and Lifelines: Add options like "50-50" or "Show hint."
Localization: Support for multiple languages.
Visual UI: Transition to a graphical user interface (e.g., with tkinter or PyQt).
## 🧪 Running Tests
Unit tests are included for all major components. Run the tests with:
```
pytest

```

## 📧 Contact
For questions or feedback, feel free to reach out to the development team.

- @nchachn
- @sajax1981
- @yhupe
- @Vanitax93
- @webboy