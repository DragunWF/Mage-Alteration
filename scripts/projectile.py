import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, origin, x_pos, y_pos):
        super().__init__()
        self.image = None

        if origin == "player":
            pass
        if origin == "enemy":
            pass

        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def movement(self):
        pass

    def visibility_check(self):
        if self.rect.x >= 825 or self.rect.y <= -35:
            self.kill()

    def update(self):
        pass
