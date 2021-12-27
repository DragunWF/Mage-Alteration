import pygame
from sys import exit
from random import randint, choice
from scripts.player import Player
from scripts.enemies import Enemies
from scripts.powerups import PowerUp
from scripts.projectile import Projectile

pygame.init()
window = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
background = pygame.image.load(
    "sprites/environment/background.png").convert_alpha()

player = pygame.sprite.GroupSingle()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

player.add(Player())


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    window.blit(background, (0, 0))

    player.update()
    player.draw(window)

    pygame.display.update()
    clock.tick(60)
