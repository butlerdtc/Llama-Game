""" V4 of game display
This version adds a font file to the directory to use an external font instead
of a system font. Makes screen dimensions variables, adds a menu font and
capitalizes all constant names.
Created by Robson Butler - 23/04/25
"""

import pygame

# Initializes pygame module
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500

# Creates the screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Loads and sets icon and caption
GAME_ICON = pygame.image.load('Images/llama_icon.png')
pygame.display.set_icon(GAME_ICON)
pygame.display.set_caption("Llama Game - By Robson Butler")

# Global variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCORE_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 20)
MENU_FONT = pygame.font.Font("PressStart2P-Regular.ttf", 30)

# Quits the module then file
pygame.quit()
quit()
