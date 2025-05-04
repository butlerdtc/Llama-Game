import pygame

pygame.init()

# Setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Llama Game - Ground v2")
clock = pygame.time.Clock()

# Load and scale ground image (double width for looping)
ground_img = pygame.transform.scale(pygame.image.load("Images/ground.png"),
                                    (SCREEN_WIDTH * 2, 100))

# Ground class with basic scrolling
class Ground:
    def __init__(self, image, y_pos):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y_pos

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.x <= -self.image.get_width() // 2:
            self.rect.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.image, (self.rect.x + self.image.get_width(), self.rect.y))

ground = Ground(ground_img, SCREEN_HEIGHT - 100)

game_speed = 5

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ground.update(game_speed)
    ground.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()