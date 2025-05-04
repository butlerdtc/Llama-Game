""" V3 of game display
Adds global variables for colour and font.
Created by Robson Butler - 22/04/25
"""

import pygame

# Initializes pygame module
pygame.init()

# Creates the screen with set dimensions
screen = pygame.display.set_mode((900, 500))

# Loads and sets icon and caption
game_icon = pygame.image.load('Images/llama_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Llama Game - By Robson Butler")

# Global variables
black = (0, 0, 0)
white = (255, 255, 255)
score_font = pygame.font.SysFont("arialblack", 20)


# Quits the module then file
pygame.quit()
quit()
