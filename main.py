import pygame
import sys
from game import Game
from ai import AI

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Tetris")

clock = pygame.time.Clock()
game = Game(WIDTH, HEIGHT)
ai = AI(game)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ai.make_move()
    game.update()

    screen.fill((0, 0, 0))
    game.draw(screen)
    pygame.display.flip()

    clock.tick(60)