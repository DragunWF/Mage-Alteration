import pygame
from .projectile import Projectile
from random import choice

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
                dmg_frame = pygame.image.load(
                    f"sprites/enemies/{enemy}_dmg.png")
                break

        right = self.image
        left = pygame.transform.flip(self.image, True, False)
        right_dmg = dmg_frame
        left_dmg = pygame.transform.flip(dmg_frame, True, False)

        self.image = right if position_x == -20 else left
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(position_x, 340))
        dmg_frame = right_dmg if position_x == -20 else left_dmg
        dmg_frame = pygame.transform.scale(dmg_frame, (64, 64))

        self.frames = (self.image, dmg_frame, dmg_frame)
        self.index = 0

        self.health = 2
        self.speed = 4 if position_x == -20 else -4
        self.direction = "left" if position_x == 820 else "right"
        self.gravity = 0
        self.cast_time = 0

        self.knockout_time = 0
        self.knockbacked = False

        if self.color == "blue":
            self.cast_sound = pygame.mixer.Sound("audio/enemyCast.ogg")
            self.cast_sound.set_volume(0.2)

    def knockback_state(self):
        self.knockout_time += 1
        self.animate_damaged()
        if self.knockout_time >= 90:
            self.knockout_time = 0
            self.knockbacked = False
            self.image = self.frames[0]

    def cast_spell(self):
        global enemy_projectiles
        self.cast_time += 1
        if self.cast_time % 60 == 0:
            self.cast_sound.play()
            enemy_projectiles.add(Projectile("enemy", self.rect.x,
                                             self.rect.y, self.direction))

    def animate_damaged(self):
        self.index += 0.2
        self.image = self.frames[int(self.index)]
        if self.index >= len(self.frames) - 1:
            self.index = 0

    def damaged(self, double_dmg):
        self.health -= 1 if not double_dmg else 2
        self.knockbacked = True
        self.is_damaged = True
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
