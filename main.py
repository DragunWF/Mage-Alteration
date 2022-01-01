import pygame
import scripts.ui_elements as ui
from sys import exit
from math import floor
from random import choice
from scripts.player import Player
from scripts.enemies import Enemy, enemy_projectiles
from scripts.powerups import PowerUp
from scripts.projectile import Projectile

pygame.init()
window = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
background = pygame.image.load(
    "sprites/environment/background.png").convert_alpha()

pygame.display.set_caption("Mage Alteration")
window_icon = pygame.image.load("sprites/player/player@2x.png").convert_alpha()
pygame.display.set_icon(window_icon)

# So we don't have to load the audio file everytime we spawn an enemy
dmg_sound = pygame.mixer.Sound("audio/damage.wav")
dmg_sound.set_volume(0.2)

game_started = False

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
scaling_timer = pygame.USEREVENT + 3
enemy_spawn_timer = pygame.USEREVENT + 4

player_cast_cooldown = pygame.USEREVENT + 5
cast_on_cooldown = False

score_timer = pygame.USEREVENT + 6
red_orbs_timer = pygame.USEREVENT + 7

player_damage_cooldown = pygame.USEREVENT + 8
player_damage_immunity = False

game_start_delay = pygame.USEREVENT + 9
game_end_delay = pygame.USEREVENT + 10

# For orb spawning
x_positions = (50, 100, 150, 200, 250, 300, 350, 400,
               450, 500, 550, 600, 650, 700, 750)


def check_collisions():
    global score_points, player_damage_immunity, game_started

    pwr_collision = pygame.sprite.spritecollide(
        player.sprite, powerups, False)
    for powerup in pwr_collision:
        player.sprite.powerup_pickup(powerup.powerup)
        powerup.kill()

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

    enemies_shot = pygame.sprite.groupcollide(
        enemies, player_projectiles, False, True)
    for enemy in enemies_shot:
        score_points += 3
        dmg_sound.play()

        dmg_check = 1 if not player.sprite.dmg_mutated else 2
        score_points += 6 if enemy.health - dmg_check <= 0 else 0

        enemy.damaged(player.sprite.dmg_mutated)

    if player.sprite:
        player.sprite.visibility_check()

    if not player.sprite:
        pygame.time.set_timer(game_end_delay, 1500)


def ui_start_menu():
    global score_points
    window.blit(*ui.StartMenu.title())
    window.blit(*ui.StartMenu.score(score_points))
    window.blit(*ui.StartMenu.play())


def ui_game_text():
    window.blit(ui.GameUI.score(score_points), (20, 15))
    health_display = player.sprite.health if player.sprite else 0
    window.blit(ui.GameUI.player_health(health_display), (20, 55))

    listings = (ui.Mutations.listing_one, ui.Mutations.listing_two,
                ui.Mutations.listing_three, ui.Mutations.listing_four)
    window.blit(ui.Mutations.mutations(), (210, 15))

    if not player.sprite.mutations:
        window.blit(ui.Mutations.no_listings(), (210, 55))
    if len(player.sprite.mutations) >= 1:
        window.blit(listings[0](player.sprite.mutations), (210, 55))
    if len(player.sprite.mutations) >= 2:
        window.blit(listings[1](player.sprite.mutations), (210, 95))
    if len(player.sprite.mutations) >= 3:
        window.blit(listings[2](player.sprite.mutations), (210, 135))
    if len(player.sprite.mutations) >= 4:
        window.blit(listings[3](player.sprite.mutations), (210, 175))


def scale_difficulty():
    global difficulty_level
    if difficulty_level >= 1:
        multiplier = difficulty_level if difficulty_level != 1 else 1.25
        factor_x = 75 if difficulty_level >= 3 else 0
        factor_y = 1500 if difficulty_level >= 4 else 50
        pygame.time.set_timer(
            enemy_spawn_timer, floor(1350 * multiplier - factor_y))
        pygame.time.set_timer(powerup_spawn_timer,
                              floor(2150 * multiplier - factor_y))
        pygame.time.set_timer(red_orbs_timer, floor(
            225 * multiplier - factor_x))
        difficulty_level -= 1


def reset_game():
    global score_points, difficulty_level
    score_points = 0
    player.add(Player())
    difficulty_level = 5  # Default: 5
    pygame.time.set_timer(game_start_delay, 1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_started:
            if event.type == game_start_delay:
                scale_difficulty()
                pygame.time.set_timer(game_start_delay, 0)
                pygame.time.set_timer(score_timer, 1000)
                pygame.time.set_timer(scaling_timer, 35000)

            if event.type == game_end_delay:
                game_started = False
                pygame.time.set_timer(enemy_spawn_timer, 0)
                pygame.time.set_timer(powerup_spawn_timer, 0)
                pygame.time.set_timer(red_orbs_timer, 0)
                pygame.time.set_timer(game_end_delay, 0)
                pygame.time.set_timer(scaling_timer, 0)

            # Player Events
            if event.type == pygame.MOUSEBUTTONDOWN and not cast_on_cooldown and player.sprite:
                player.sprite.cast_sound.play()
                cast_origin = "mutated" if player.sprite.dmg_mutated else "player"
                player_projectiles.add(Projectile(
                    cast_origin, player.sprite.rect.x,
                    player.sprite.rect.y, player.sprite.direction))

                if player.sprite.cast_mutated:
                    other_direction = "right" if player.sprite.direction == "left" else "left"
                    player_projectiles.add(Projectile(
                        cast_origin, player.sprite.rect.x,
                        player.sprite.rect.y, other_direction))

                cast_on_cooldown = True
                pygame.time.set_timer(player_cast_cooldown, 175)

            if event.type == player_cast_cooldown:
                cast_on_cooldown = False
                pygame.time.set_timer(player_cast_cooldown, 0)

            if event.type == player_damage_cooldown:
                player_damage_immunity = False
                pygame.time.set_timer(player_damage_cooldown, 0)

            # Main Events
            if event.type == score_timer and player.sprite:
                score_points += 1

            if event.type == scaling_timer:
                scale_difficulty()

            if event.type == enemy_spawn_timer:
                enemies.add(Enemy())

            if event.type == powerup_spawn_timer:
                powerups.add(PowerUp())

            if event.type == red_orbs_timer:
                red_projectiles.add(Projectile(
                    "sky", choice(x_positions), -20, ""))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_started = True
                reset_game()

    window.blit(background, (0, 0))

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

    if player.sprite:
        ui_game_text()
        check_collisions()

    if not game_started:
        ui_start_menu()
        pygame.time.set_timer(score_timer, 0)
        pygame.time.set_timer(scaling_timer, 0)

    pygame.display.update()
    clock.tick(60)
