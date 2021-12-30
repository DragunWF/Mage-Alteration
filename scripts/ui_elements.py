import pygame

pygame.init()

font = "fonts/kenneyPixel.ttf"
font_sizes = (25, 50, 75, 100)

game_text = pygame.font.Font(font, font_sizes[1], bold=True)
title_text = pygame.font.Font(font, font_sizes[3], bold=True)


def player_health(hp_value):
    return game_text.render(f"Health: {hp_value}", (0, 0), (1, 184, 234))


def score(score):
    return game_text.render(f"Score: {score}", (0, 0), (1, 184, 234))


def mutations(powerups):
    pass
