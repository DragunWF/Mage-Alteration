import pygame

pygame.init()

font = "fonts/kenneyPixel.ttf"
font_sizes = (25, 50, 75, 100)

game_text = pygame.font.Font(font, font_sizes[1], bold=True)
title_text = pygame.font.Font(font, font_sizes[3], bold=True)

light_cyan = (1, 184, 234)


def player_health(hp_value):
    return game_text.render(f"Health: {hp_value}", (0, 0), light_cyan)


def score(score):
    return game_text.render(f"Score: {score}", (0, 0), light_cyan)


def mutations(powerups):
    return game_text.render(
        f"""
Mutations:
{powerups}""", (0, 0), light_cyan)
