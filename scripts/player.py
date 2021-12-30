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

        self.speed_time, self.speed_mutated = 0, False
        self.super_jump_time, self.jump_mutated = 0, False
        self.back_shot_time, self.cast_mutated = 0, False
        self.mutations = []

        self.dmg_sound = pygame.mixer.Sound("audio/damage.wav")
        self.cast_sound = pygame.mixer.Sound("audio/cast.ogg")
        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
        self.pick_up_sound = pygame.mixer.Sound("audio/pickUp.wav")

        self.dmg_sound.set_volume(0.2)
        self.cast_sound.set_volume(0.2)
        self.jump_sound.set_volume(0.1)
        self.pick_up_sound.set_volume(0.5)

    def mutated_state(self):
        if self.speed_mutated:
            self.speed_time += 1
            self.speed = 10
            if self.speed_time >= 60 * 15:
                self.speed_mutated = False
                self.speed = 5
                self.speed_time = 0
                self.mutations.pop(self.mutations.index("Speed"))

        if self.jump_mutated:
            self.super_jump_time += 1
            self.jump_force = -25
            if self.super_jump_time >= 60 * 20:
                self.jump_mutated = False
                self.jump_force = -17
                self.super_jump_time = 0
                self.mutations.pop(
                    self.mutations.index("Increased Jump Height"))

        if self.cast_mutated:
            self.back_shot_time += 1
            # Add code here for the rear casting logic
            if self.back_shot_time >= 60 * 10:
                self.back_shot_mutated = False
                self.back_shot_time = 0
                self.mutations.pop(self.mutations.index("Rear Casting"))

    def powerup_pickup(self, powerup):
        self.pick_up_sound.play()

        if powerup == "health":
            self.health += 1

        if powerup == "speed":
            self.speed_mutated = True
            self.speed_time = 0
            if "Speed" not in self.mutations:
                self.mutations.append("Speed")

        if powerup == "superJump":
            self.jump_mutated = True
            self.super_jump_time = 0
            if "Increased Jump Height" not in self.mutations:
                self.mutations.append("Increased Jump Height")

        if powerup == "backShot":
            self.cast_mutated = True
            self.back_shot_time = 0
            if "Rear Casting" not in self.mutations:
                self.mutations.append("Rear Casting")

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
        if self.speed_mutated or self.jump_mutated or self.cast_mutated:
            self.mutated_state()
        self.apply_gravity()
        self.movement()
