import pygame

pygame.init()

# Setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Llama Game - Ground v1")
clock = pygame.time.Clock()

# Load and scale ground image
ground_image = pygame.transform.scale(pygame.image.load("Images/ground.png"),
                                      (SCREEN_WIDTH, 100))

# Initial ground position
ground_x = 0
ground_y = SCREEN_HEIGHT - 100

# Game speed
game_speed = 5

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ground position
    ground_x -= game_speed
    if ground_x <= -SCREEN_WIDTH:
        ground_x = 0

    # Draw ground once
    screen.blit(ground_image, (ground_x, ground_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()