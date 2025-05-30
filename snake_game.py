import pygame
import random
import sys
import os
import math
from pathlib import Path

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Game speeds for different difficulty levels
EASY_FPS = 8
MEDIUM_FPS = 12
HARD_FPS = 16

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
GRAY = (100, 100, 100)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Create sounds directory if it doesn't exist
sounds_dir = Path("sounds")
sounds_dir.mkdir(exist_ok=True)

# Sound system using custom MP3 files
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.sounds_enabled = True
        
        # List of sound files to load
        sound_files = {
            "eat": "eat.mp3",
            "special": "special.mp3",
            "level_up": "level_up.mp3",
            "game_over": "game_over.mp3"
        }
        
        # Load sound files
        for name, filename in sound_files.items():
            path = sounds_dir / filename
            if path.exists():
                try:
                    self.sounds[name] = pygame.mixer.Sound(str(path))
                    print(f"Loaded sound: {name}")
                except Exception as e:
                    print(f"Error loading sound {name}: {e}")
            else:
                print(f"Sound file not found: {filename}")
        
        # Load background music
        self.bg_music_path = sounds_dir / "background.mp3"
        
        if not self.sounds:
            print("No sound files found. Sound disabled.")
            self.sounds_enabled = False
    
    def play_background_music(self):
        if self.sounds_enabled and self.bg_music_path.exists():
            try:
                pygame.mixer.music.load(str(self.bg_music_path))
                pygame.mixer.music.set_volume(0.3)  # Lower volume for background music
                pygame.mixer.music.play(-1)  # Loop indefinitely
                print("Background music started")
            except Exception as e:
                print(f"Error playing background music: {e}")
    
    def play(self, sound_name):
        if not self.sounds_enabled:
            return
            
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def eat_sound(self):
        self.play("eat")
    
    def special_sound(self):
        self.play("special")
    
    def level_up_sound(self):
        self.play("level_up")
    
    def game_over_sound(self):
        self.play("game_over")

# Create sound manager
sound_manager = SoundManager()

# High score file
HIGH_SCORE_FILE = "snake_high_score.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
        
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check if snake hits the wall
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False
        
        # Check if snake hits itself
        if new_head in self.body:
            return False
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True
    
    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def grow_snake(self):
        self.grow = True
    
    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            color = GREEN if i == 0 else (0, 200, 0)  # Head is slightly different color
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Border

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
        self.type = self.generate_type()
        
    def generate_position(self, snake_body):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position not in snake_body:
                return position
    
    def generate_type(self):
        # 70% normal food, 20% bonus food, 10% special food
        rand = random.random()
        if rand < 0.7:
            return "normal"  # Normal food (1 point)
        elif rand < 0.9:
            return "bonus"   # Bonus food (2 points)
        else:
            return "special" # Special food (5 points)
    
    def get_points(self):
        if self.type == "normal":
            return 1
        elif self.type == "bonus":
            return 2
        else:  # special
            return 5
    
    def get_color(self):
        if self.type == "normal":
            return RED
        elif self.type == "bonus":
            return BLUE
        else:  # special
            return GOLD
    
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.get_color(), rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # Border

def draw_text(surface, text, size, x, y, color=WHITE, center=False):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)
    return text_rect

def difficulty_selection():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game - Select Difficulty")
    clock = pygame.time.Clock()
    
    difficulties = ["Easy", "Medium", "Hard"]
    selected = 1  # Default to Medium
    
    while True:
        screen.fill(BLACK)
        
        draw_text(screen, "SNAKE GAME", 72, WIDTH//2, HEIGHT//4, center=True)
        draw_text(screen, "Select Difficulty:", 48, WIDTH//2, HEIGHT//2 - 60, center=True)
        
        # Draw difficulty options
        for i, diff in enumerate(difficulties):
            if i == selected:
                color = GREEN
            else:
                color = WHITE
            draw_text(screen, diff, 36, WIDTH//2, HEIGHT//2 + i*50, color=color, center=True)
        
        draw_text(screen, "Use UP/DOWN arrows or W/S to select, ENTER to confirm", 24, 
                 WIDTH//2, HEIGHT*3//4 + 50, center=True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return EASY_FPS
                    elif selected == 1:
                        return MEDIUM_FPS
                    else:
                        return HARD_FPS
        
        pygame.display.flip()
        clock.tick(10)

def draw_pause_menu(surface):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))
    
    # Draw pause menu text
    draw_text(surface, "PAUSED", 72, WIDTH//2, HEIGHT//2 - 50, center=True)
    draw_text(surface, "Press SPACE to resume", 36, WIDTH//2, HEIGHT//2 + 30, center=True)
    draw_text(surface, "Press Q to quit", 36, WIDTH//2, HEIGHT//2 + 80, center=True)

def game_loop(initial_fps):
    # Set up the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    # Create game objects
    snake = Snake()
    food = Food(snake.body)
    
    # Game variables
    score = 0
    high_score = load_high_score()
    game_over = False
    paused = False
    
    # Level system
    level = 1
    foods_eaten = 0
    foods_for_level_up = 5
    current_fps = initial_fps
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        return "restart"  # Restart the game
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_SPACE:  # Pause game with SPACE key
                    paused = not paused
                elif event.key == pygame.K_q and paused:  # Quit from pause menu
                    pygame.quit()
                    sys.exit()
                elif not paused:  # Only allow control when not paused
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.change_direction(RIGHT)
        
        if not game_over and not paused:
            # Move the snake
            if not snake.move():
                game_over = True
                sound_manager.game_over_sound()
                
                # Update high score if needed
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
            
            # Check if snake eats food
            if snake.body[0] == food.position:
                snake.grow_snake()
                points = food.get_points()
                score += points
                
                # Play appropriate sound
                if food.type == "normal":
                    sound_manager.eat_sound()
                else:
                    sound_manager.special_sound()
                
                # Level up system
                foods_eaten += 1
                if foods_eaten >= foods_for_level_up:
                    level += 1
                    foods_eaten = 0
                    current_fps += 2  # Increase speed with each level
                    sound_manager.level_up_sound()
                    
                    # Flash level notification without pausing gameplay
                    # We'll just show it in the UI instead of a full animation
                
                food = Food(snake.body)
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw grid (optional)
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))
        
        # Draw game objects
        snake.draw(screen)
        food.draw(screen)
        
        # Draw score, high score and level
        draw_text(screen, f"Score: {score}", 36, 10, 10)
        draw_text(screen, f"High Score: {high_score}", 36, 10, 50)
        
        # Draw level with highlight if recently changed
        level_color = GOLD if foods_eaten == 0 and level > 1 else WHITE
        draw_text(screen, f"Level: {level}", 36, WIDTH - 150, 10, color=level_color)
        draw_text(screen, f"Speed: {current_fps}", 24, WIDTH - 150, 50)
        
        # Draw controls reminder
        draw_text(screen, "Controls: Arrows or WASD", 18, WIDTH - 200, HEIGHT - 25)
        
        # Draw foods eaten progress
        progress_width = 200
        progress_height = 20
        progress_x = WIDTH - progress_width - 10
        progress_y = 80
        
        # Draw progress bar background
        pygame.draw.rect(screen, GRAY, (progress_x, progress_y, progress_width, progress_height))
        
        # Draw progress bar fill
        fill_width = int((foods_eaten / foods_for_level_up) * progress_width)
        pygame.draw.rect(screen, GREEN, (progress_x, progress_y, fill_width, progress_height))
        
        # Draw progress bar border
        pygame.draw.rect(screen, WHITE, (progress_x, progress_y, progress_width, progress_height), 2)
        
        # Draw progress text
        draw_text(screen, f"Next Level: {foods_eaten}/{foods_for_level_up}", 24, progress_x + 10, progress_y + 25)
        
        # Draw pause menu if paused
        if paused:
            draw_pause_menu(screen)
        
        # Game over screen
        if game_over:
            draw_text(screen, "GAME OVER", 72, WIDTH//2, HEIGHT//2 - 50, center=True)
            
            if score == high_score and score > 0:
                draw_text(screen, "NEW HIGH SCORE!", 48, WIDTH//2, HEIGHT//2 + 10, color=GOLD, center=True)
            
            draw_text(screen, "Press R to Restart or Q to Quit", 36, 
                     WIDTH//2, HEIGHT//2 + 70, center=True)
        
        pygame.display.flip()
        clock.tick(current_fps)

def main():
    # Start background music
    sound_manager.play_background_music()
    
    while True:
        # Select difficulty
        fps = difficulty_selection()
        
        # Start game with selected difficulty
        result = game_loop(fps)
        
        if result != "restart":
            break

if __name__ == "__main__":
    main()
