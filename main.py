import pygame
import scripts.ui_elements as ui
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

main_menu = False
in_game = True

score = 0
difficulty_level = 0

player = pygame.sprite.GroupSingle()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()

player_damage_cooldown = pygame.USEREVENT + 1
powerup_spawn_timer = pygame.USEREVENT + 2
scaling_difficulty_timer = pygame.USEREVENT + 3
enemy_spawn_timer = pygame.USEREVENT + 4

player_cast_cooldown = pygame.USEREVENT + 5
cast_on_cooldown = False

# ---------- For Testing Purposes ----------
pygame.time.set_timer(enemy_spawn_timer, 1500)
player.add(Player())
# ------------------------------------------


def check_collisions():
    global score
    if player.sprite:
        if pygame.sprite.spritecollide(player.sprite, enemies, False):
            player.sprite.damaged()

    enemies_shot = pygame.sprite.groupcollide(
        enemies, player_projectiles, False, True)
    for enemy in enemies_shot:
        score += 3
        enemy.kill()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Player Events
        if event.type == pygame.MOUSEBUTTONDOWN and not cast_on_cooldown:
            player_projectiles.add(Projectile(
                "player", player.sprite.rect.x,
                player.sprite.rect.y, player.sprite.direction))
            cast_on_cooldown = True
            pygame.time.set_timer(player_cast_cooldown, 250)
        if event.type == player_cast_cooldown:
            cast_on_cooldown = False
            pygame.time.set_timer(player_cast_cooldown, 0)
        if event.type == player_damage_cooldown:
            pass

        # Misc Events
        if event.type == enemy_spawn_timer:
            enemies.add(Enemy())
        if event.type == powerup_spawn_timer:
            pass
        if event.type == scaling_difficulty_timer:
            pass

    window.blit(background, (0, 0))

    window.blit(ui.score(score), (25, 25))

    player_projectiles.update()
    player_projectiles.draw(window)

    player.update()
    player.draw(window)

    enemies.update()
    enemies.draw(window)

    powerups.update()
    powerups.draw(window)

    check_collisions()

    pygame.display.update()
    clock.tick(60)
