import pygame
from random import randint, choice


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        color = choice(("red", "blue"))
        position_x = choice((-20, 820))

        if color == "red":
            self.image = pygame.image.load("sprites/enemies/red.png")
        if color == "blue":
            self.image = pygame.image.load("sprites/enemies/blue.png")

        right = self.image
        left = pygame.transform.flip(self.image, True, False)

        self.image = right if position_x == -20 else left
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(position_x, 340))

        self.health = 2
        self.speed = 4 if position_x == -20 else -4
        self.gravity = 0

    def damaged(self):
        pass

    def movement(self):
        self.rect.x += self.speed

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 352:
            self.rect.bottom = 352

    def update(self):
        self.apply_gravity()
        self.movement()
