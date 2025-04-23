""" V4 of game display
This version adds a font file to the directory to use an external font instead
of a system font. Makes screen dimensions variables.
Created by Robson Butler - 23/04/25
"""

import pygame

# Initializes pygame module
pygame.init()

# Screen dimensions
screen_width = 900
screen_height = 600

# Creates the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Loads and sets icon and caption
game_icon = pygame.image.load('Images/llama_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Llama Game - By Robson Butler")

# Global variables
black = (0, 0, 0)
white = (255, 255, 255)
score_font = pygame.font.Font("PressStart2P-Regular.ttf", 20)


# Quits the module then file
pygame.quit()
quit()
