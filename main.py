import pygame
from sys import exit
from random import randint, choice
from scripts.player import Player
from scripts.enemies import Enemy
from scripts.powerups import PowerUp
from scripts.projectile import Projectile

pygame.init()
window = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
background = pygame.image.load(
    "sprites/environment/background.png").convert_alpha()

player = pygame.sprite.GroupSingle()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

player_damage_cooldown = pygame.USEREVENT + 1
powerup_spawn_timer = pygame.USEREVENT + 2
scaling_difficulty_timer = pygame.USEREVENT + 3
enemy_spawn_timer = pygame.USEREVENT + 4


def check_collisions():
    if player.sprite and player.sprite.health > 0:
        if pygame.sprite.spritecollide(player.sprite, enemies, False):
            player.sprite.damaged()


# ---------- For Testing Purposes ----------
pygame.time.set_timer(enemy_spawn_timer, 1500)
player.add(Player())
# ------------------------------------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == player_damage_cooldown:
            pass
        if event.type == enemy_spawn_timer:
            enemies.add(Enemy())
            print("Enemy spawned")
        if event.type == powerup_spawn_timer:
            pass
        if event.type == scaling_difficulty_timer:
            pass
        if event.type == enemy_spawn_timer:
            pass

    window.blit(background, (0, 0))

    player.update()
    player.draw(window)

    enemies.update()
    enemies.draw(window)

    projectiles.update()
    projectiles.draw(window)

    powerups.update()
    powerups.draw(window)

    pygame.display.update()
    clock.tick(60)