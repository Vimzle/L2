import pygame
from game import Game

pygame.init()

screen = pygame.display.set_mode((400, 250))
pygame.display.set_caption("Ragdoll Game")
clock = pygame.time.Clock()
game = Game(screen)


running = True
while running:
    dt = clock.tick(60) / 1000

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    game.handle_input(keys, dt)
    game.update(dt)
    if game.is_game_over():
        running = False
    game.draw()
    pygame.display.flip()

pygame.quit()
