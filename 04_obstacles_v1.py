import pygame

pygame.init()

# Setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Llama Game - Obstacle v1")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

# Load a single cactus image
cactus_img = pygame.transform.scale(pygame.image.load("Images/cactus.png"), (64, 64))

# Basic obstacle setup
obstacle_x = SCREEN_WIDTH
obstacle_y = SCREEN_HEIGHT - 100  # Ground level
game_speed = 5

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move obstacle
    obstacle_x -= game_speed

    # Reset obstacle once it leaves screen
    if obstacle_x < -64:
        obstacle_x = SCREEN_WIDTH

    # Draw cactus
    screen.blit(cactus_img, (obstacle_x, obstacle_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
