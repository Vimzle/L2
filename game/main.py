import pygame
from ragdoll import Ragdoll
from field import GameField

pygame.init()
FIELD_WIDTH = 400
FIELD_HEIGHT = 250
screen = pygame.display.set_mode((FIELD_WIDTH, FIELD_HEIGHT))
pygame.display.set_caption("Ragdoll Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 20)  

cat_img = pygame.image.load("assets/ragdoll.png").convert_alpha()
treat_img = pygame.image.load("assets/fish.png").convert_alpha()  
cat_mask = pygame.mask.from_surface(cat_img)
treat_mask = pygame.mask.from_surface(treat_img)

ragdoll = Ragdoll(FIELD_WIDTH, FIELD_HEIGHT, cat_img.get_width())
field = GameField(FIELD_WIDTH, FIELD_HEIGHT, treat_img.get_width())

score = 0

running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill((94, 33, 41))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    ragdoll.move(dx, dy, dt)

    field.move_treats(ragdoll, cat_mask, treat_mask, dt)
    score += field.collect_treats(ragdoll, cat_mask, treat_mask)
    ragdoll.decrease_satiety(dt)
    if ragdoll.satiety == 0:
        running = False

    for treat in field._treats:
        screen.blit(treat_img, (treat["x"], treat["y"]))
    screen.blit(cat_img, (ragdoll.x, ragdoll.y))
    ###
    score_text = font.render(f"Съедено рыбок: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    bar_width, bar_height = int((ragdoll.satiety / ragdoll.MAX_SATIETY) * 60), 15
    bar_x = field.width - bar_width - 10
    bar_y = 10
    pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    bar_text = font.render("Сытость", True, (0, 0, 0))
    screen.blit(bar_text, (bar_x - bar_text.get_width() - 5,
                    bar_y + (bar_height - bar_text.get_height()) // 2))
    ###
    pygame.display.flip()

pygame.quit()
