import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, origin, x_pos, y_pos, direction):
        super().__init__()
        self.direction = direction
        self.origin = origin

        if origin == "player":
            frame_1 = pygame.image.load(
                "sprites/projectiles/green/green_1.png").convert_alpha()
            frame_2 = pygame.image.load(
                "sprites/projectiles/green/green_2.png").convert_alpha()
            frame_3 = pygame.image.load(
                "sprites/projectiles/green/green_3.png").convert_alpha()
            frame_4 = pygame.image.load(
                "sprites/projectiles/green/green_4.png").convert_alpha()
            frame_5 = pygame.image.load(
                "sprites/projectiles/green/green_5.png").convert_alpha()
        if origin == "enemy":
            pass

        self.frames = (frame_1, frame_2, frame_3, frame_4,
                       frame_5, frame_5, frame_5, frame_4,
                       frame_3, frame_2, frame_1)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x_pos, y_pos + 7.5))

    def movement(self):
        self.rect.x += 8.5 if self.direction == "right" else -8.5

    def animate(self):
        if self.index >= len(self.frames) - 1:
            self.index = 0
        self.index += 0.4
        self.image = self.frames[int(self.index)]
        self.image = pygame.transform.scale(self.image, (40, 40))

    def visibility_check(self):
        if self.rect.x >= 825 or self.rect.x <= -35:
            self.kill()

    def update(self):
        self.movement()
        self.animate()
        self.visibility_check()
