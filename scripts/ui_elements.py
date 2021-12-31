import pygame

pygame.init()

font = "fonts/kenneyPixel.ttf"
font_sizes = (25, 50, 75, 100)

# mutation_text = pygame.font.Font(font, font_sizes[0], bold=True)
game_text = pygame.font.Font(font, font_sizes[1], bold=True)
title_text = pygame.font.Font(font, font_sizes[3], bold=True)

light_cyan = (1, 184, 234)


class Mutations:
    def mutations():
        return game_text.render("Mutations:", (0, 0), light_cyan)

    def no_listings():
        return game_text.render("None", (0, 0), light_cyan)

    def listing_one(powerups):
        return game_text.render(powerups[0], (0, 0), light_cyan)

    def listing_two(powerups):
        return game_text.render(powerups[1], (0, 0), light_cyan)

    def listing_three(powerups):
        return game_text.render(powerups[2], (0, 0), light_cyan)


def player_health(hp_value):
    return game_text.render(f"Health: {hp_value}", (0, 0), light_cyan)


def score(score):
    return game_text.render(f"Score: {score}", (0, 0), light_cyan)
