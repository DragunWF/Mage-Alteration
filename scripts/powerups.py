import pygame
from random import choice


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        powerup_types = ("health", "speed", "backShot", "superJump")
        x_positions = (50, 100, 150, 200, 250, 300, 350, 400,
                       450, 500, 550, 600, 650, 700, 750)
        self.powerup = choice(powerup_types)

        self.image = pygame.image.load(f"sprites/powerups/{self.powerup}.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(center=(choice(x_positions), -20))

    def visibility_check(self):
        if self.rect.y >= 425:
            print("delete powerup")
            self.kill()

    def movement(self):
        self.rect.y += 2

    def update(self):
        self.movement()
        self.visibility_check()
