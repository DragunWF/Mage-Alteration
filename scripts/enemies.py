import pygame
from random import randint, choice


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_types = ("red", "blue")
        color = choice(enemy_types)
        position_x = choice((-20, 820))

        for enemy in enemy_types:
            if color == enemy:
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

    def knockback_state(self):
        pass

    def damaged(self):
        self.health -= 1
        if self.health < 1:
            self.kill()

    def visibility_check(self):
        if self.rect.x >= 840 or self.rect.x <= -50:
            self.kill()

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
        self.visibility_check()
