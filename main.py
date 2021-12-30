import pygame
import scripts.ui_elements as ui
from sys import exit
from random import randint, choice
from scripts.player import Player
from scripts.enemies import Enemy
from scripts.enemies import enemy_projectiles
from scripts.powerups import PowerUp
from scripts.projectile import Projectile

pygame.init()
window = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
background = pygame.image.load(
    "sprites/environment/background.png").convert_alpha()

window_icon = pygame.image.load("sprites/player/player@2x.png").convert_alpha()
pygame.display.set_icon(window_icon)

# So we don't have to load the audio file everytime we spawn an enemy
dmg_sound = pygame.mixer.Sound("audio/damage.wav")
dmg_sound.set_volume(0.2)

start_menu = False
game_started = True

score_points = 0
difficulty_level = 0

player = pygame.sprite.GroupSingle()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player_projectiles = pygame.sprite.Group()
red_projectiles = pygame.sprite.Group()
blue_projectiles = pygame.sprite.Group()

player_damage_cooldown = pygame.USEREVENT + 1
powerup_spawn_timer = pygame.USEREVENT + 2
scaling_difficulty_timer = pygame.USEREVENT + 3
enemy_spawn_timer = pygame.USEREVENT + 4

player_cast_cooldown = pygame.USEREVENT + 5
cast_on_cooldown = False

score_timer = pygame.USEREVENT + 6
bad_orbs_timer = pygame.USEREVENT + 7

player_damage_cooldown = pygame.USEREVENT + 8
player_damage_immunity = False

# For orb spawning
x_positions = (50, 100, 150, 200, 250, 300, 350, 400,
               450, 500, 550, 600, 650, 700, 750)

# ---------- For Testing Purposes ----------
pygame.time.set_timer(enemy_spawn_timer, 1500)
pygame.time.set_timer(powerup_spawn_timer, 1000)
pygame.time.set_timer(score_timer, 1000)
pygame.time.set_timer(bad_orbs_timer, 1000)
player.add(Player())
# ------------------------------------------


def check_collisions():
    global score_points, player_damage_immunity

    if player.sprite:
        enemy_collision = pygame.sprite.spritecollide(
            player.sprite, enemies, False)
        rp_collision = pygame.sprite.spritecollide(
            player.sprite, red_projectiles, True)
        ep_collision = pygame.sprite.spritecollide(
            player.sprite, enemy_projectiles, True)
        if not player_damage_immunity and (enemy_collision or rp_collision or ep_collision):
            player.sprite.damaged()
            player_damage_immunity = True
            pygame.time.set_timer(player_damage_cooldown, 1000)

        pwr_collision = pygame.sprite.spritecollide(
            player.sprite, powerups, False)
        for powerup in pwr_collision:
            player.sprite.powerup_pickup(powerup.powerup)
            powerup.kill()

    enemies_shot = pygame.sprite.groupcollide(
        enemies, player_projectiles, False, True)
    for enemy in enemies_shot:
        score_points += 3
        dmg_sound.play()
        enemy.damaged()


def main_menu():
    pass


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Player Events
        if event.type == pygame.MOUSEBUTTONDOWN and not cast_on_cooldown:
            player.sprite.cast_sound.play()
            player_projectiles.add(Projectile(
                "player", player.sprite.rect.x,
                player.sprite.rect.y, player.sprite.direction))
            cast_on_cooldown = True
            pygame.time.set_timer(player_cast_cooldown, 250)

        if event.type == player_cast_cooldown:
            cast_on_cooldown = False
            pygame.time.set_timer(player_cast_cooldown, 0)

        if event.type == player_damage_cooldown:
            player_damage_immunity = False
            pygame.time.set_timer(player_damage_cooldown, 0)

        # Main Events
        if event.type == score_timer and player.sprite:
            score_points += 1

        if event.type == enemy_spawn_timer:
            enemies.add(Enemy())

        if event.type == powerup_spawn_timer:
            powerups.add(PowerUp())

        if event.type == scaling_difficulty_timer:
            pass

        if event.type == bad_orbs_timer:
            red_projectiles.add(Projectile(
                "sky", choice(x_positions), -20, ""))

    window.blit(background, (0, 0))

    window.blit(ui.score(score_points), (20, 15))

    if player.sprite:
        window.blit(ui.player_health(player.sprite.health), (20, 55))
    else:
        window.blit(ui.player_health(0, (20, 55)))

    player_projectiles.update()
    player_projectiles.draw(window)

    enemy_projectiles.update()
    enemy_projectiles.draw(window)

    red_projectiles.update()
    red_projectiles.draw(window)

    player.update()
    player.draw(window)

    enemies.update()
    enemies.draw(window)

    powerups.update()
    powerups.draw(window)

    check_collisions()

    pygame.display.update()
    clock.tick(60)
