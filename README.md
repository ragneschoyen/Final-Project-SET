# Final-Project-SET
This project implements the SET card game in Python using Pygame. 

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
SET is a card game where the goal is to find a set of 3 cards from the 12 cards displayed on the screen. Each card has three properties; color, symbol, shading, and number. For 3 cards to be a set, either all properties needs to be the same or all different on the three cards. 

## Installation
1. Clone the repository:
```bash
 git clone https://github.com/ragneschoyen/Final-Project-SET
```

2. Install dependencies:
```bash
 pip install pygame
 ```

3. Run the game:
To run the project, use the following command:
```bash
python main.py
```

## Usage
When you start the game, a Pygame window will open. The window will display 12 cards, you use your keyboard to input the number corresponding to the 3 cards you think is a SET. You will also see a timer counting down from 30, when the time is up, and you did not find a SET, you will see if the computer found one, if it did the coumputer gets a point and a new round starts. If you find a SET, before the time is up, you get a point and a new round starts. If there are no SETs on the table, the top three cards gets replaced, and the timer starts over. Each time a set is found either by the player or the computer, the set is replaced with 3 new cards. This goes on for 15 rounds, and then it is game over, and the winner of the game is displayed. 

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

