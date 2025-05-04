import pygame
import random

pygame.init()

# Constants from 01_display_v4
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_ICON = pygame.image.load('Images/llama_icon.png')
pygame.display.set_icon(GAME_ICON)
pygame.display.set_caption("Llama Game - By Robson Butler")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCORE_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 20)
MENU_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 30)

clock = pygame.time.Clock()

# List for if more obstacles are added in future
obstacles = []

cactus_picture = pygame.transform.scale(pygame.image.load("Images/cactus.png"),
                                        (64, 64))

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


# Main routine
game_speed_temp = 5

# Sets the frame count and base time between obstacle spawns
frame_count = 0
next_obstacle_spawn_time = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Increases frame count by each frame (60 per second)
    frame_count += 1

    # Intervals for varying obstacle spawn times
    base_interval = max(20, int(60 - game_speed_temp * 2))  # 24 - 40
    min_interval = 45
    max_interval = min(150, base_interval + 50)  # 74 - 90

    if frame_count >= next_obstacle_spawn_time:  # Every second minimum
        # 80% chance to spawn an obstacle
        if random.random() < 0.8:
            # Creates obstacle
            obstacles.append(Obstacle(cactus_picture, 200))
        # Sets next obstacle spawn based on base value and variance
        next_obstacle_spawn_time = frame_count + random.randint(
            min_interval, max_interval)  # 30 - 90

    # Removes obstacle when it moves off-screen
    for obstacle in list(obstacles):
        should_remove = obstacle.update(game_speed_temp)
        if should_remove:
            obstacles.remove(obstacle)

    SCREEN.fill(WHITE)

    # Draw all active obstacles
    for obstacle in obstacles:
        obstacle.draw(SCREEN)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()
