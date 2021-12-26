import pygame
from sys import exit
from random import randint, choice
from scripts.player import Player
from scripts.enemies import Enemies
from scripts.powerups import PowerUp
from scripts.projectile import Projectile

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()

test = pygame.image.load("sprites/red/red.png").convert_alpha()
test = pygame.transform.scale(test, (64, 64))

while True:
    screen.blit(test, (400, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)
