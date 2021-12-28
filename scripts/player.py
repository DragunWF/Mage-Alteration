import pygame
from math import floor


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.speed = 5
        self.jump_force = -15

        self.image = pygame.image.load(
            "sprites/player/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(400, 150))

        self.default_img = self.image
        self.flipped_img = pygame.transform.flip(self.image, True, False)

        self.gravity = 0
        self.spell_cooldown = 0

        self.dmg_sound = pygame.mixer.Sound("audio/damage.wav")
        self.cast_sound = pygame.mixer.Sound("audio/cast.ogg")

    def damaged(self):
        pass

    def movement(self):
        key = pygame.key.get_pressed()
        diagonal_speed, speed = self.speed * 0.75, self.speed
        if key[pygame.K_SPACE] and self.rect.bottom >= 352:
            self.gravity = self.jump_force
        if key[pygame.K_d]:
            self.rect.x += speed
            self.image = self.default_img
        elif key[pygame.K_a]:
            self.rect.x -= speed
            self.image = self.flipped_img

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 352:
            self.rect.bottom = 352

    def visibility_check(self):
        if self.rect.x >= 815 or self.rect.x <= -15:
            self.kill()

    def update(self):
        self.apply_gravity()
        self.movement()
