# Snake Game Creation Guide

This README provides a step-by-step guide to creating a Snake game using Pygame,  
following these 10 prompts.

## Game Creation Prompts

1. Make a snake game window that's 600x600 with a black background. Use a grid  
with 20x20 squares and set up colors like green for the snake and red for food.

2. Create a snake that moves around using arrow keys or WASD. Make it grow  
longer when it eats food and die if it hits walls or itself.

3. Add different types of food - regular red food worth 1 point, blue bonus food  
worth 2 points, and gold special food worth 5 points that appear randomly.

4. Make the controls work so the snake moves in the direction you press, but don't  
let it do a complete 180° turn into itself.

5. Add a score counter at the top of the screen and save the highest score to a  
file so players can try to beat their record.

6. Create a start screen where players can pick Easy, Medium or Hard difficulty  
that changes how fast the snake moves.

7. Make a level system where the snake speeds up after eating 5 pieces of food,  
and show what level you're on.

8. Add a progress bar that fills up as you eat food to show how close you are to  
the next level.

9. Put in sound effects for eating food, getting special food, leveling up, and  
game over. Add some background music too.

10. Add a pause button (spacebar) that shows a menu, and a game over screen that  
lets you restart with the R key or quit with Q.

11. Add fullscreen support with resizable window functionality. In fullscreen mode,  
the grid squares automatically resize to be larger for better gameplay experience.

## How to Run the Game

### Prerequisites
- Python 3.x installed on your system  
- Pygame library installed

### Installation
1. If you don't have Pygame installed, install it using pip:

```bash
pip install pygame
```

2. Create a directory structure for your game:

```bash
Snake_Game/
├── snake_game.py
└── sounds/
    ├── eat.mp3
    ├── special.mp3
    ├── level_up.mp3
    ├── game_over.mp3
    └── background.mp3
```

3. Add your sound files to the `sounds` directory (the game will run without sounds but they enhance the experience).

### Running the Game
1. Navigate to the game directory in your terminal or command prompt:

```bash
cd path/to/Snake_Game
```

2. Run the game:

```bash
python snake_game.py
```

### Game Controls
- Use arrow keys or WASD to control the snake  
- Press SPACE to pause the game  
- When game is over, press R to restart or Q to quit

### Window Controls
- Use your operating system's window controls to resize the game window
- To enter fullscreen mode:
  - On macOS: Click the green button in the top-left corner
  - On Windows: Click the maximize button or drag the window to the top edge
- In fullscreen mode, grid squares automatically become larger for better gameplay
- The game adapts to any window size while maintaining proper proportions

### Game Features
- Three difficulty levels: Easy, Medium, and Hard  
- Progressive level system with increasing speed  
- Three types of food with different point values  
- High score tracking  
- Sound effects and background music  
- Visual progress tracking toward next level
- Fullscreen support with adaptive grid sizing
- Resizable window that maintains gameplay balance

Enjoy playing your Snake game!
