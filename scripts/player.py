import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 5
        self.speed = 5
        self.jump_force = -17

        self.image = pygame.image.load(
            "sprites/player/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(400, -50))

        dmg_img = pygame.image.load("sprites/player/player_dmg.png")
        dmg_img = pygame.transform.scale(dmg_img, (64, 64))
        self.frames_right = (self.image, dmg_img, dmg_img)

        def scale(image):
            return pygame.transform.flip(image, True, False)

        self.frames_left = tuple(map(scale, self.frames_right))
        self.index = 0

        self.default_img = self.image
        self.flipped_img = pygame.transform.flip(self.image, True, False)
        self.direction = "right"

        self.damaged_time = 0
        self.is_damaged = False

        self.gravity = 0
        self.spell_cooldown = 0

        self.speed_time, self.speed_mutated = 0, False
        self.super_jump_time, self.jump_mutated = 0, False
        self.rear_casting_time, self.cast_mutated = 0, False
        self.double_dmg_time, self.dmg_mutated = 0, False
        self.mutations = []

        self.dmg_sound = pygame.mixer.Sound("audio/damage.wav")
        self.cast_sound = pygame.mixer.Sound("audio/cast.ogg")
        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
        self.pick_up_sound = pygame.mixer.Sound("audio/pickUp.wav")
        self.lose_sound = pygame.mixer.Sound("audio/lose.wav")

        self.dmg_sound.set_volume(0.2)
        self.cast_sound.set_volume(0.2)
        self.jump_sound.set_volume(0.1)
        self.pick_up_sound.set_volume(0.5)
        self.lose_sound.set_volume(0.6)

    def animate_damaged(self):
        self.index += 0.2
        if self.direction == "right":
            self.image = self.frames_right[int(self.index)]
        else:
            self.image = self.frames_left[int(self.index)]
        if self.index >= len(self.frames_right) - 1:
            self.index = 0

    def damaged_state(self):
        self.damaged_time += 1
        if self.damaged_time >= 60:
            self.damaged_time = 0
            self.is_damaged = False

    def damaged(self):
        self.dmg_sound.play()
        self.health -= 1
        self.is_damaged = True
        if self.health < 1:
            self.lose_sound.play()
            self.kill()

    def animate(self):
        if not self.is_damaged:
            if self.direction == "right":
                self.image = self.default_img
            else:
                self.image = self.flipped_img
        else:
            self.animate_damaged()
            self.damaged_state()

    def mutated_state(self):
        if self.speed_mutated:
            self.speed_time += 1
            self.speed = 8
            if self.speed_time >= 60 * 15:
                self.speed_mutated = False
                self.speed = 5
                self.speed_time = 0
                self.mutations.pop(self.mutations.index("+Speed"))

        if self.jump_mutated:
            self.super_jump_time += 1
            self.jump_force = -21
            if self.super_jump_time >= 60 * 20:
                self.jump_mutated = False
                self.jump_force = -17
                self.super_jump_time = 0
                self.mutations.pop(
                    self.mutations.index("+Jump Height"))

        if self.cast_mutated:
            self.rear_casting_time += 1
            if self.rear_casting_time >= 60 * 7:
                self.cast_mutated = False
                self.rear_casting_time = 0
                self.mutations.pop(self.mutations.index("Rear Casting"))

        if self.dmg_mutated:
            self.double_dmg_time += 1
            if self.double_dmg_time >= 60 * 8:
                self.dmg_mutated = False
                self.double_dmg_time = 0
                self.mutations.pop(self.mutations.index("Double Damage"))

    def powerup_pickup(self, powerup):
        self.pick_up_sound.play()

        if powerup == "health":
            self.health += 1

        if powerup == "speed":
            self.speed_mutated = True
            self.speed_time = 0
            if "+Speed" not in self.mutations:
                self.mutations.append("+Speed")

        if powerup == "superJump":
            self.jump_mutated = True
            self.super_jump_time = 0
            if "+Jump Height" not in self.mutations:
                self.mutations.append("+Jump Height")

        if powerup == "backShot":
            self.cast_mutated = True
            self.rear_casting_time = 0
            if "Rear Casting" not in self.mutations:
                self.mutations.append("Rear Casting")

        if powerup == "doubleDmg":
            self.dmg_mutated = True
            self.double_dmg_time = 0
            if "Double Damage" not in self.mutations:
                self.mutations.append("Double Damage")

    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.rect.bottom >= 352:
            self.gravity = self.jump_force
            self.jump_sound.play()
        if key[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = "right"
        elif key[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = "left"

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 352:
            self.rect.bottom = 352

    def visibility_check(self):
        if self.rect.x >= 825 or self.rect.x <= -25:
            self.lose_sound.play()
            self.kill()

    def update(self):
        if self.speed_mutated or self.jump_mutated or self.cast_mutated:
            self.mutated_state()
        self.apply_gravity()
        self.movement()
        self.visibility_check()
        self.animate()
