class Ragdoll:
    SPEED = 100
    MAX_SATIETY = 100

    def __init__(self, field_width, field_height, ragdoll_size):
        # TODO: бодрость/энергия
        self.satiety = self.MAX_SATIETY
        self.x = 0
        self.y = 0
        self.max_x = field_width - ragdoll_size
        self.max_y = field_height - ragdoll_size

    def move(self, dx, dy, dt):
        self.x += dx * self.SPEED * dt
        self.y += dy * self.SPEED * dt
        self.x = max(0, min(self.max_x, self.x))
        self.y = max(0, min(self.max_y, self.y))

    def increase_satiety(self, amount):
        self.satiety = min(self.MAX_SATIETY, self.satiety + amount)

    def decrease_satiety(self, dt, decay_rate=8):
        self.satiety -= decay_rate * dt
        if self.satiety < 0:
            self.satiety = 0
