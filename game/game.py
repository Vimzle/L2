import pygame
from ragdoll import Ragdoll
from treat import TreatManager

class Game:
    FIELD_WIDTH = 400
    FIELD_HEIGHT = 250
    def __init__(self, screen):
        self.screen = screen
        self.font = font = pygame.font.SysFont("Comic Sans MS", 20)  

        self.cat_img = pygame.image.load("assets/ragdoll.png").convert_alpha()
        self.treat_img = pygame.image.load("assets/fish.png").convert_alpha()  

        self.cat_mask = pygame.mask.from_surface(self.cat_img)
        self.treat_mask = pygame.mask.from_surface(self.treat_img)

        self.ragdoll = Ragdoll(self.FIELD_WIDTH, self.FIELD_HEIGHT, self.cat_img.get_width(), self.cat_mask, self.treat_mask)
        self.treat_manager = TreatManager(self.FIELD_WIDTH, self.FIELD_HEIGHT, self.treat_img.get_width())

        self.score = 0
        self.game_over = False

    def handle_input(self, keys, dt):
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.ragdoll.move(dx, dy, dt)

    def update(self, dt):
        if self.game_over: return
        self.ragdoll.decrease_satiety(dt)
        self.treat_manager.move_treats(self.ragdoll, dt)
        score = self.treat_manager.collect_treats(self.ragdoll)
        if score > 0:
            self.ragdoll.increase_satiety(20 * score)
            self.score += score
        if self.ragdoll.satiety <= 0:
            self.game_over = True

    def draw(self):
        self.screen.fill((94, 33, 41))
        for treat in self.treat_manager.treats:
            self.screen.blit(self.treat_img, (treat.x, treat.y))
        self.screen.blit(self.cat_img, (self.ragdoll.x, self.ragdoll.y))

        score_text = self.font.render(f"Съедено рыбок: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10,10))

        bar_width, bar_height = int((self.ragdoll.satiety / self.ragdoll.MAX_SATIETY) * 60), 15
        bar_x = self.FIELD_WIDTH - bar_width - 10
        bar_y = 10
        pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        bar_text = self.font.render("Сытость", True, (0, 0, 0))
        self.screen.blit(bar_text, (bar_x - bar_text.get_width() - 5,
                        bar_y + (bar_height - bar_text.get_height()) // 2))
    
    def is_game_over(self):
        return self.game_over