import pygame

pygame.init()

screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Llama Game v2")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)

# Load images
llama_run = [
    pygame.transform.scale(pygame.image.load("Images/Llama3.png"), (70, 70)),
    pygame.transform.scale(pygame.image.load("Images/Llama2.png"), (70, 70))
]
llama_jump = pygame.transform.scale(pygame.image.load("Images/Llama.png"), (70, 70))

gravity = 1
jump_strength = 20

class Llama:
    def __init__(self):
        self.run_imgs = llama_run
        self.jump_img = llama_jump
        self.image = self.run_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = 400
        self.y_velocity = 0
        self.jumping = False
        self.frame = 0

    def update(self, keys):
        # Jumping input
        if keys[pygame.K_SPACE] and not self.jumping:
            self.y_velocity = -jump_strength
            self.jumping = True

        # Gravity
        self.y_velocity += gravity
        self.rect.y += self.y_velocity

        # Land
        if self.rect.y >= 400:
            self.rect.y = 400
            self.y_velocity = 0
            self.jumping = False

        # Image switching
        if self.jumping:
            self.image = self.jump_img
        else:
            self.frame = (self.frame + 1) % 10
            self.image = self.run_imgs[self.frame // 5]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

llama = Llama()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    llama.update(keys)
    llama.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
