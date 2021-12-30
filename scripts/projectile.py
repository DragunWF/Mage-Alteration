import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, origin, x_pos, y_pos, direction):
        super().__init__()
        self.direction = direction
        self.origin = origin
        pairs = {"player": "green", "enemy": "blue", "sky": "red"}

        for key in pairs:
            if origin == key:
                color = pairs[key]
                break

        frame_1 = pygame.image.load(
            f"sprites/projectiles/{color}/{color}_1.png").convert_alpha()
        frame_2 = pygame.image.load(
            f"sprites/projectiles/{color}/{color}_2.png").convert_alpha()
        frame_3 = pygame.image.load(
            f"sprites/projectiles/{color}/{color}_3.png").convert_alpha()
        frame_4 = pygame.image.load(
            f"sprites/projectiles/{color}/{color}_4.png").convert_alpha()
        frame_5 = pygame.image.load(
            f"sprites/projectiles/{color}/{color}_5.png").convert_alpha()

        def scale(image):
            return pygame.transform.scale(image, (40, 40))

        self.frames = (frame_1, frame_2, frame_3, frame_4,
                       frame_5, frame_5, frame_5, frame_4,
                       frame_3, frame_2, frame_1)
        self.index = 0

        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x_pos + 4, y_pos + 7.5))

        self.frames = tuple(map(scale, self.frames))
        # I placed it after calling the rect function so I can make the
        # projectile collision smaller

    def movement(self):
        if self.origin != "sky":
            self.rect.x += 8.5 if self.direction == "right" else -8.5
        else:
            self.rect.y += 5

    def animate(self):
        if self.index >= len(self.frames) - 1:
            self.index = 0
        self.index += 0.25
        self.image = self.frames[int(self.index)]

    def delete_conditions(self):
        if self.rect.x >= 825 or self.rect.x <= -35 or self.rect.y >= 425:
            print("delete projectile")
            self.kill()

    def update(self):
        self.movement()
        self.animate()
        self.delete_conditions()
