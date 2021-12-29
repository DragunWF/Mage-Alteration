import pygame

pygame.init()

font_sizes = (25, 50, 75, 100)

font = pygame.font.Font("fonts/kenneyPixel.ttf", font_sizes[1], bold=True)


def score(score):
    return font.render(f"Score: {score}", (25, 25), (1, 184, 234))
