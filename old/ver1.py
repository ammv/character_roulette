import pygame
import random

from time import sleep
from threading import Thread

WIDTH = 800  # ширина игрового окна
HEIGHT = 450 # высота игрового окна
FPS = 30 # частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

COLORS = (BLACK, WHITE, BLUE)

pygame.init()
#pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character roulette")
clock = pygame.time.Clock()

current_color = 0

running = True
while running:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
                
    screen.fill(COLORS[current_color % len(COLORS)])
    pygame.display.flip()
    
    current_color += 1
    
pygame.quit()