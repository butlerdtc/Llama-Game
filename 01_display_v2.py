""" V2 of game display
Adds caption and icon to window. Uses time module for testing.
Created by Robson Butler - 22/04/25
"""

import pygame
# Time module for testing purposes
import time

# Initializes pygame module
pygame.init()

# Creates the screen with set dimensions
screen = pygame.display.set_mode((900, 600))

game_icon = pygame.image.load('Images/llama_icon.png')

pygame.display.set_icon(game_icon)
pygame.display.set_caption("Llama Game - By Robson Butler")

# Delays quit by 3 seconds to test if icons and captions work
time.sleep(3)


# Quits the module then file
pygame.quit()
quit()
