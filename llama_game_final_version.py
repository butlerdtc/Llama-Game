"""Final version of the llama game """

import pygame
import random
import time

# Initializes pygame module
pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font for score and messages
SCORE_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 20)
MENU_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 30)

# Physics constants
GRAVITY = 1 # How much vertical velocity changes each frame due to gravity
JUMP_STRENGTH = 20 # Initial upward velocity when jumping
OBSTACLE_BASE_SPEED = 10 # Base speed at which obstacles move

# Game icon and caption
GAME_ICON = pygame.image.load('Images/llama_icon.png')
pygame.display.set_icon(GAME_ICON)
pygame.display.set_caption("Llama Game - By Robson Butler")


# Class for handling the score system and game factors like speed and deaths.
class GameState:
    def __init__(self):
        self.game_speed = OBSTACLE_BASE_SPEED
        self.points = 0
        self.start_time = 0
        self.obstacles = []
        self.death_count = 0
        self.high_score = GameState.load_high_score()

    # Static method to keep track of high score in a text file
    @staticmethod
    def load_high_score():
        try:
            # Opens text file so the score can be read then closes the file
            with open("HI_score.txt", 'r') as hi_score_file:
                content = hi_score_file.read().strip()
                # If content is a number, it returns it as an integer or 0
                if content.isdigit():
                    return int(content)
                return 0
        # Creates the file if it does not already exist
        except IOError:
            with open("HI_score.txt", 'w') as hi_score_file:
                hi_score_file.write("0")
                return 0

    # Method to update the high score
    def update_high_score(self):
        # Max returns the largest of the arguments
        self.high_score = max(self.points, self.high_score)

    # Method to save the high score to the text file
    def save_high_score(self):
        try:
            with open("HI_score.txt", 'w') as high_score_file:
                high_score_file.write(str(int(self.high_score)))
        except IOError:
            print("Error saving high score to HI_score.txt")

    # Method to reset attributes to their originals
    def reset_game_state(self):
        self.game_speed = OBSTACLE_BASE_SPEED
        self.points = 0
        self.start_time = time.time()
        self.obstacles = []


# Class to create and handle the llama character and its uses
class Llama:
    # Constant X position of the llama on the screen
    X_POSITION = 80

    def __init__(self, llama_run_img, llama_jump_img, ground_top):
        # Sets the llamas images to the images passed into the class
        self.run_img = llama_run_img
        self.jump_img = llama_jump_img

        # Flags to check if llama is running or jumping (Running by default)
        self.running = True
        self.jumping = False

        # Llama movement variables
        self.y_velocity = 0 # Counts velocity during jumping
        self.step_index = 0 # Tracks frames for running animation

        # Llama image properties
        self.image = self.run_img[0] # Starts with the first running image
        self.llama_rect = self.image.get_rect() # Get rectangle for position
        self.llama_rect.x = self.X_POSITION # Sets llamas x position
        self.llama_rect.bottom = ground_top - 1 # Starts on the ground

    # Method to update the llamas movements
    def update(self, user_input, ground_top):
        # Adds gravity to the Y velocity to make it fall once in air
        self.y_velocity += GRAVITY

        # Update vertical position based on velocity
        self.llama_rect.y += self.y_velocity

        # Checks for landing on the ground
        if self.llama_rect.bottom >= ground_top - 1:
            self.llama_rect.bottom = ground_top - 1 # Snap to ground level
            self.y_velocity = 0 # Stop falling
            if self.jumping: # Only transition if it was jumping
                 self.jumping = False
                 self.running = True # Return to running state

        # Check for jump input
        if user_input[pygame.K_SPACE] and not self.jumping:
             self.jump() # Call the jump method to initiate a jump

        # Handle animation based on state
        if self.running:
            self.run_animation()
        elif self.jumping:
            self.image = self.jump_img # Show jump image while jumping

        # Handle animation frame cycling for running
        if self.running:
             self.step_index += 1
             # Cycle through frames, 5 frames per image
             if self.step_index >= len(self.run_img) * 5:
                 self.step_index = 0

    # Method to make the running animation for the llama
    def run_animation(self):
        # Set image based on animation step for running
        self.image = self.run_img[self.step_index // 5]
        # Update rectangle size based on the current image for drawing
        self.llama_rect.width = self.image.get_width()
        self.llama_rect.height = self.image.get_height()
        # Ensures X position is unchanged
        self.llama_rect.x = self.X_POSITION

    # Method to initiate the llama jumping
    def jump(self):
        # Negative because y-axis increases downwards
        self.y_velocity = -JUMP_STRENGTH
        # Changes flags to indicate llama has started jumping
        self.jumping = True
        self.running = False

    # Method to draw the llama image at its rectangle's top-left position
    def draw(self, screen):
        screen.blit(self.image, (self.llama_rect.x, self.llama_rect.y))

    # Method to get the rect for collision outside the class
    def get_llama_rect(self):
        # This gets the rectangle of the actual picture on screen without the
        # transparent edges for a more accurate collision
        bounding_rect = self.image.get_bounding_rect()
        bounding_rect.x += self.llama_rect.x
        bounding_rect.y += self.llama_rect.y
        return bounding_rect


# Class to create and run the obstacles
class Obstacle:
    def __init__(self, image, ground_top):
        self.image = image # Sets the obstacle image as an attribute
        self.rect = self.image.get_rect() # Get rectangle for position
        # Spawns off-screen to the right
        self.rect.x = SCREEN_WIDTH + random.randint(100, 300)
        self.rect.bottom = ground_top  # Positions on the ground level

    # Method to update the obstacles position
    def update(self, game_speed):
        # Moves obstacle to the left based on game speed
        self.rect.x -= game_speed
        # Checks if the obstacle has gone off-screen
        if self.rect.x < -self.rect.width:
            return True # Indicate that the obstacle should be removed
        return False # Indicate that the obstacle should not be removed

    # Method to draw the obstacle
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Gets the hitbox of the obstacle for collisions
    def get_obstacle_rect(self):
        bounding_rect = self.image.get_bounding_rect()
        bounding_rect.x += self.rect.x
        bounding_rect.y += self.rect.y
        # Inflates by negative to shrink hitbox for more accurate collisions
        shrunk_rect = bounding_rect.inflate(-20, -20)
        return shrunk_rect


# Class to create and move the ground
class Ground:
    def __init__(self, ground_img, ground_y_pos):
        self.image = ground_img
        self.rect = self.image.get_rect()
        self.rect.x = 0 # Start at the left edge
        self.rect.y = ground_y_pos # Position at the ground level

    # Method to update ground position
    def update(self, game_speed):
        # Moves ground to the left based on game speed
        self.rect.x -= game_speed
        # Checks if the ground has completely moved off-screen then resets
        if self.rect.x <= -self.image.get_width():
             self.rect.x = 0 # Reset to start

    # Method to draw the ground
    def draw(self, screen):
        # Draws the ground image twice for seamless scrolling
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.image, (self.rect.x + self.image.get_width(),
                                 self.rect.y))


# Image loading and scaling function
def load_and_scale(path, size):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(),
                                  size)


# Function to get the images used
def get_images():
    llama_run_img = [load_and_scale("Images/Llama3.png", (70, 70)),
                     load_and_scale("Images/Llama2.png", (70, 70))
                     ]

    llama_jump_img = load_and_scale("Images/Llama.png", (70, 70))

    cactus_img = load_and_scale("Images/cactus.png", (64, 64))

    ground_img = load_and_scale("Images/ground.png",
                                (SCREEN_WIDTH * 2, 400))
    return llama_run_img, llama_jump_img, cactus_img, ground_img


# Displays the current score and high score for the game
def display_score(game_state, screen):
    score_to_show = SCORE_FONT.render(f"Score:{game_state.points}",
                                      True, BLACK)
    score_rect = score_to_show.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    screen.blit(score_to_show, score_rect)

    display_high_score = SCORE_FONT.render(f"High Score:{game_state.high_score}",
                                      True, BLACK)
    high_score_rect = display_high_score.get_rect(topleft=(20, 20))
    screen.blit(display_high_score, high_score_rect)


# Function to get, update and then display score
def get_and_update_score(game_state, screen):
    # Gets the current time
    current_time = time.time()
    # Tracks number of seconds since start of game. 10 points per second
    game_state.points = int((current_time - game_state.start_time) * 10)

    # Updates high score attribute for game state
    game_state.update_high_score()

    # Increases speed based on survival time
    speed_increase = min((game_state.points // 10) * 0.2, 8)
    game_state.game_speed = OBSTACLE_BASE_SPEED + speed_increase

    # Runs the display score function
    display_score(game_state, screen)


# Main game loop
def main(llama_run_img, llama_jump_img, cactus_img, ground_img):
    # Loads and resets the game state and attributes
    game_state = GameState()
    game_state.reset_game_state()

    # Loads ground properties
    ground_height = ground_img.get_height()
    ground_y_pos = SCREEN_HEIGHT - ground_height
    ground_line_offset = int(ground_height * 0.59)
    ground_top = ground_y_pos + ground_line_offset

    # Initialize flag and clock for framerate
    run = True
    clock = pygame.time.Clock()

    # Create the player instance
    player = Llama(llama_run_img, llama_jump_img, ground_top)

    # Create the ground instance
    ground_ = Ground(ground_img, ground_y_pos)

    # Sets the frame count and base time between obstacle spawns
    frame_count = 0
    next_obstacle_spawn_time = 60

    # Game loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # End the game loop if window is closed

        # Get keyboard input
        user_input = pygame.key.get_pressed()

        # Updates player (based on input) and ground
        player.update(user_input, ground_top)
        ground_.update(game_state.game_speed)

        # Increases frame count by each frame (60 per second)
        frame_count += 1

        # Intervals for varying obstacle spawn times
        base_interval = max(20, int(60 - game_state.game_speed * 2)) # 24 - 40
        min_interval = 45
        max_interval = min(150, base_interval + 50) # 74 - 90

        if frame_count >= next_obstacle_spawn_time: # Every second minimum
            # 80% chance to spawn an obstacle
            if random.random() < 0.8:
                # Creates obstacle
                game_state.obstacles.append(Obstacle(cactus_img, ground_top))
            # Sets next obstacle spawn based on base value and variance
            next_obstacle_spawn_time = frame_count + random.randint(
                min_interval, max_interval) # 30 - 90

        # Removes obstacle when it moves off-screen
        for obstacle in list(game_state.obstacles):
            should_remove = obstacle.update(game_state.game_speed)
            if should_remove:
                  game_state.obstacles.remove(obstacle)

            # Gets the llama and obstacle hitbox
            llama_hitbox = player.get_llama_rect()
            obstacle_hitbox = obstacle.get_obstacle_rect()

            # Detects if llama collides with obstacle
            if llama_hitbox.colliderect(obstacle_hitbox):
                # Collision detected so death count increases and score saves
                game_state.death_count += 1
                game_state.save_high_score()

                # Delay by 1 second then run menu
                pygame.time.delay(1000)

                # Call the menu function to handle game over screen and restart
                menu(game_state, llama_run_img, llama_jump_img, cactus_img,
                     ground_img)
                return # Exit the main game loop when menu is called

        SCREEN.fill(WHITE) # Fill background
        ground_.draw(SCREEN) # Draw ground
        player.draw(SCREEN) # Draw llama

        # Draw all active obstacles
        for obstacle in game_state.obstacles:
            obstacle.draw(SCREEN)

        # Updates the score and displays it
        get_and_update_score(game_state, SCREEN)

        pygame.display.update()

        # Sets the framerate
        clock.tick(60)

    # Saves high score
    game_state.save_high_score()

    # Quit game
    pygame.quit()
    quit()


# Menu function
def menu(game_state, llama_run_img, llama_jump_img, cactus_img, ground_img):
    # Flag while game runs
    run = True
    while run:
        SCREEN.fill(WHITE)

        # Determine text based on whether it's the first start or a restart
        if game_state.death_count == 0:
            # Text for starting game and quitting game
            text = MENU_FONT.render("Press SPACE to Start", True,
                                    BLACK)
            quit_text = MENU_FONT.render("Press 'Q' to Quit",
                                         True, BLACK)
            quit_text_rect = quit_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        else:
            # Text for restarting, displaying score and quitting
            text = MENU_FONT.render("Press SPACE to Restart",
                                    True, BLACK)

            # Current score text and position
            score_text = SCORE_FONT.render(f"Your Score:"
                                           f"{game_state.points}",
                                           True, BLACK)
            score_rect = score_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            SCREEN.blit(score_text, score_rect)

            # High score text and position
            high_score_text = SCORE_FONT.render(f"High Score:"
                                                f"{game_state.high_score}",
                                                True, BLACK)
            high_score_rect = high_score_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            SCREEN.blit(high_score_text, high_score_rect)

            # Quitting text and position
            quit_text = MENU_FONT.render("Press 'Q' to Quit",
                                         True, BLACK)
            quit_text_rect = quit_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

        # Positions the text message
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2,
                                          SCREEN_HEIGHT // 2 + 10))
        SCREEN.blit(text, text_rect)
        SCREEN.blit(quit_text, quit_text_rect)

        # Checks if image was loaded
        if llama_run_img:
            # Positions a llama image for during the menu
             standing_llama_menu = llama_jump_img
             llama_menu_rect = standing_llama_menu.get_rect(
                 center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
             SCREEN.blit(standing_llama_menu, llama_menu_rect)

        # Update the display
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Saves the high score to text file
                game_state.save_high_score()
                pygame.quit()
                quit()

            # Check for key press
            if event.type == pygame.KEYDOWN:
                # If user selects 'Q' saves high score then quits game
                if event.key == pygame.K_q:
                    game_state.save_high_score()
                    pygame.quit()
                    quit()

                # If user selects 'SPACE' it will run the game
                if event.key == pygame.K_SPACE:
                    main(llama_run_img, llama_jump_img, cactus_img, ground_img)
                    return


# Main routine
initial_game_state = GameState()

# Sets death count to 0
initial_game_state.death_count = 0

# Loads the images
llama_run_image, llama_jump_image, cactus_image, ground_image = get_images()

# Runs the menu
menu(initial_game_state, llama_run_image, llama_jump_image, cactus_image,
     ground_image)
