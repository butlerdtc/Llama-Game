import pygame

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

ground_picture = pygame.transform.scale(pygame.image.load("Images/ground.png"),
                                        (SCREEN_WIDTH * 2, 400))

# Temporary colour for testing
RED = (255, 0, 0)


# Class to create and move the ground
class Ground:
    def __init__(self, ground_img, ground_y_pos):
        self.image = ground_img
        self.rect = self.image.get_rect()
        self.rect.x = 0 # Start at the left edge
        self.rect.y = ground_y_pos # Position at the ground level

        # Temporary attributes for dot for testing
        self.dot_offset_x = 450
        self.dot_offset_y = 240
        self.dot_radius = 10

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

        # Dot drawing for testing
        dot_pos_x = self.rect.x + self.dot_offset_x
        dot_pos_y = self.rect.y + self.dot_offset_y

        pygame.draw.circle(screen, RED, (dot_pos_x, dot_pos_y), self.dot_radius, 0)

        dot_pos_x_second = self.rect.x + self.image.get_width() + self.dot_offset_x
        dot_pos_y_second = self.rect.y + self.dot_offset_y

        if dot_pos_x_second > -self.dot_radius:
            pygame.draw.circle(screen, RED, (dot_pos_x_second, dot_pos_y_second), self.dot_radius, 0)

        line_start_y = self.rect.y
        line_end_y = self.rect.y + self.image.get_height()

        line_1_x = self.rect.x
        pygame.draw.line(screen, BLACK, (line_1_x, line_start_y), (line_1_x, line_end_y), 2)

        line_2_x = self.rect.x + self.image.get_width()
        pygame.draw.line(screen, BLACK, (line_2_x, line_start_y),
                         (line_2_x, line_end_y), 2)


# Main routine
# Ground properties
ground_height = ground_picture.get_height()
ground_y_position = SCREEN_HEIGHT - ground_height

ground = Ground(ground_picture, ground_y_position)

# Temporary game speed
game_speed_temp = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ground.update(game_speed_temp)

    SCREEN.fill(WHITE)
    ground.draw(SCREEN)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()
