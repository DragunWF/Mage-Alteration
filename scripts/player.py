import pygame
from math import floor


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.speed = 5
        self.jump_force = -17

        self.image = pygame.image.load(
            "sprites/player/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(400, -50))

        self.default_img = self.image
        self.flipped_img = pygame.transform.flip(self.image, True, False)
        self.direction = "right"

        self.gravity = 0
        self.spell_cooldown = 0
        self.mutations = []

        self.dmg_sound = pygame.mixer.Sound("audio/damage.wav")
        self.cast_sound = pygame.mixer.Sound("audio/cast.ogg")
        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")

        self.dmg_sound.set_volume(0.2)
        self.cast_sound.set_volume(0.2)
        self.jump_sound.set_volume(0.1)

    def damage_cooldown(self):
        pass

    def damaged(self):
        self.dmg_sound.play()
        self.health -= 1

    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.rect.bottom >= 352:
            self.gravity = self.jump_force
            self.jump_sound.play()
        if key[pygame.K_d]:
            self.rect.x += self.speed
            self.image = self.default_img
            self.direction = "right"
        elif key[pygame.K_a]:
            self.rect.x -= self.speed
            self.image = self.flipped_img
            self.direction = "left"

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
