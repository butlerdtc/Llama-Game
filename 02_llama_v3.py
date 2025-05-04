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

# Physics constants
GRAVITY = 1
JUMP_STRENGTH = 20

# Images for the llama
llama_run = [
    pygame.transform.scale(pygame.image.load("Images/Llama3.png"),
                           (70, 70)), pygame.transform.scale(
        pygame.image.load("Images/Llama2.png"), (70, 70))]

llama_jump = pygame.transform.scale(pygame.image.load("Images/Llama.png"),
                                    (70, 70))

clock = pygame.time.Clock()

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
        self.llama_rect.bottom = ground_top # Starts on the ground

    # Method to update the llamas movements
    def update(self, user_input, ground_top):
        # Adds gravity to the Y velocity to make it fall once in air
        self.y_velocity += GRAVITY

        # Update vertical position based on velocity
        self.llama_rect.y += self.y_velocity

        # Checks for landing on the ground
        if self.llama_rect.bottom >= ground_top:
            self.llama_rect.bottom = ground_top
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


# Main routine
llama = Llama(llama_run, llama_jump, 400)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    user_key_pressed = pygame.key.get_pressed()

    llama.update(user_key_pressed, 400)

    SCREEN.fill(WHITE)
    llama.draw(SCREEN)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()
