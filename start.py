import pygame
import os
import sys
from demin import play_game

# dimensions de l'écran
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# options de taille de grille
GRID_SIZES = [10, 20, 30]

# initialisation de Pygame
pygame.init()

# configuration de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Démineur")

def draw_button(surface, text, x, y, w, h, color):
    pygame.draw.rect(surface, color, (x, y, w, h))
    font = pygame.font.Font(None, 24)
    text_render = font.render(text, 1, (0, 0, 0))
    surface.blit(text_render, (x + w / 2 - text_render.get_width() / 2, y + h / 2 - text_render.get_height() / 2))

def main_menu():
    buttons = []
    for i, grid_size in enumerate(GRID_SIZES):
        rect = pygame.Rect(200, 150 + i * 100, 200, 50)
        buttons.append((rect, grid_size))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button[0].collidepoint(event.pos):
                        play_game(button[1])
                        return

        screen.fill((255, 255, 255))
        for button in buttons:
            draw_button(screen, f'Jouer avec une grille de taille {button[1]}', *button[0], (173, 216, 230))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
