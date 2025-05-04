import pygame
import random

pygame.init()

# Setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Llama Game - Obstacle v2")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

cactus_img = pygame.transform.scale(pygame.image.load("Images/cactus.png"), (64, 64))
game_speed = 5

# Obstacle class with basic logic
class Obstacle:
    def __init__(self, image, ground_y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 200)
        self.rect.y = ground_y

    def update(self, speed):
        self.rect.x -= speed
        return self.rect.right < 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

obstacles = []
frame_counter = 0
spawn_interval = 90

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_counter += 1

    if frame_counter >= spawn_interval:
        obstacles.append(Obstacle(cactus_img, SCREEN_HEIGHT - 100))
        frame_counter = 0

    for obs in list(obstacles):
        if obs.update(game_speed):
            obstacles.remove(obs)
        obs.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
