import pygame
from random import randint, choice


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        color = choice(("red", "blue"))
        position_x = choice(())

        if color == "red":
            self.image = pygame.image.load("sprites/enemies/red.png")
        if color == "blue":
            self.image = pygame.image.load("sprites/enemies/blue.png")

        self.rect = self.image.get_rect(center=(position_x, 340))
        
