import pygame

pygame.init()

# Setup
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Llama Game v1")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)

# Load one llama image
llama_img = pygame.image.load("Images/Llama.png")
llama_img = pygame.transform.scale(llama_img, (70, 70))

# Physics constants
gravity = 1
jump_strength = 20

# Llama setup
llama_y = 400
y_velocity = 0
jumping = False

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not jumping:
        y_velocity = -jump_strength
        jumping = True

    # Gravity
    y_velocity += gravity
    llama_y += y_velocity

    # Ground collision
    if llama_y >= 400:
        llama_y = 400
        y_velocity = 0
        jumping = False

    # Draw llama
    screen.blit(llama_img, (80, llama_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
