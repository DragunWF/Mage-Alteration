import pygame
from math import floor


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.health = 3
        self.speed = 5
        self.image = None
        self.rect = None

    def movement(self):
        speed = self.speed
        diagonal_speed = self.speed * 0.75

    def update(self):
        pass
