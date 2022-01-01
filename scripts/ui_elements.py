import pygame

pygame.init()

font = "fonts/kenneyPixel.ttf"
font_sizes = (25, 50, 75, 100)

game_text = pygame.font.Font(font, font_sizes[1], bold=True)
title_text = pygame.font.Font(font, font_sizes[3], bold=True)

light_cyan = (1, 184, 234)


class Mutations:
    def mutations():
        return game_text.render("Mutations:", True, light_cyan)

    def no_listings():
        return game_text.render("None", True, light_cyan)

    def listing_one(powerups):
        return game_text.render(powerups[0], True, light_cyan)

    def listing_two(powerups):
        return game_text.render(powerups[1], True, light_cyan)

    def listing_three(powerups):
        return game_text.render(powerups[2], True, light_cyan)

    def listing_four(powerups):
        return game_text.render(powerups[3], True, light_cyan)


class StartMenu:
    def title():
        text = title_text.render("Mage Alteration", True, light_cyan)
        rect = text.get_rect(center=(400, 100))
        return text, rect

    def score(score):
        text = title_text.render(f"Score: {score}", True, light_cyan)
        rect = text.get_rect(center=(400, 200))
        return text, rect

    def play():
        text = title_text.render("Press Enter to play", True, light_cyan)
        rect = text.get_rect(center=(400, 300))
        return text, rect


class GameUI:
    def player_health(hp_value):
        return game_text.render(f"Health: {hp_value}", True, light_cyan)

    def score(score):
        return game_text.render(f"Score: {score}", True, light_cyan)
