import pygame
from game import Game

pygame.init()

pygame.display.set_caption("Ragdoll Game")
clock = pygame.time.Clock()
game = Game()


running = True
while running:
    dt = clock.tick(60) / 1000

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.VIDEORESIZE:
            new_size = min(e.w, e.h)
            game.resizable.update(new_size)
            game.cat_img_scaled = game.resizable.scale_image(game.cat_img)
            game.treat_img_scaled = game.resizable.scale_image(game.treat_img)
            game.ghost_img_scaled = game.resizable.scale_image(game.ghost_img)
            game.cat_mask = pygame.mask.from_surface(game.cat_img_scaled)
            game.treat_mask = pygame.mask.from_surface(game.treat_img_scaled)
            game.ghost_mask = pygame.mask.from_surface(game.ghost_img_scaled)
            game.ragdoll.cat_mask = game.cat_mask
            game.ragdoll.treat_mask = game.treat_mask
            game.ghost_manager.ghost_mask = game.ghost_mask

    keys = pygame.key.get_pressed()
    game.handle_input(keys, dt)
    game.update(dt)
    if game.is_game_over():
        running = False
    game.draw()
    pygame.display.flip()

pygame.quit()
