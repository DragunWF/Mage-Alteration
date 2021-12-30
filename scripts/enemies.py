import pygame
import math
from .projectile import Projectile
from random import randint, choice

enemy_projectiles = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_types = ("red", "red", "red", "blue", "blue")
        position_x = choice((-20, 820))
        self.color = choice(enemy_types)

        for enemy in enemy_types:
            if self.color == enemy:
                self.image = pygame.image.load(f"sprites/enemies/{enemy}.png")
                break

        right = self.image
        left = pygame.transform.flip(self.image, True, False)

        self.image = right if position_x == -20 else left
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(position_x, 340))

        self.health = 2
        self.speed = 4 if position_x == -20 else -4
        self.direction = "left" if position_x == 820 else "right"
        self.gravity = 0
        self.cast_time = 0

        self.knockout_time = 0
        self.knockbacked = False

    def knockback_state(self):
        self.knockout_time += 1
        if self.knockout_time >= 90:
            self.knockout_time = 0
            self.knockbacked = False

    def cast_spell(self):
        global enemy_projectiles
        self.cast_time += 1
        if self.cast_time % 60 == 0:
            enemy_projectiles.add(Projectile("enemy", self.rect.x,
                                             self.rect.y, self.direction))

    def damaged(self):
        self.health -= 1
        self.rect.x += -15 if self.direction == "right" else 15
        self.knockbacked = True
        if self.health < 1:
            self.kill()

    def visibility_check(self):
        if self.rect.x >= 840 or self.rect.x <= -50:
            self.kill()

    def movement(self):
        if not self.knockbacked:
            self.rect.x += self.speed
        else:
            self.rect.x += self.speed - 3 if self.direction == "right" else -3
            self.knockback_state()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 352:
            self.rect.bottom = 352

    def update(self):
        if self.color == "blue":
            self.cast_spell()
        self.movement()
        self.apply_gravity()
        self.visibility_check()
