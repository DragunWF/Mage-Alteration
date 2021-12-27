import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, origin, x_pos, y_pos):
        self.image = None

        if origin == "player":
            pass
        if origin == "enemy":
            pass

        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def movement(self):
        pass

    def update(self):
        pass
