class Ragdoll():
    SPEED = 100
    MAX_SATIETY = 100

    def __init__(self, ragdoll_size, cat_mask, treat_mask, resizable):
        self.ref_ragdoll_size = ragdoll_size
        self.satiety = self.MAX_SATIETY
        self.ref_x = 0
        self.ref_y = 0
        self.cat_mask = cat_mask
        self.treat_mask = treat_mask
        self.resizable = resizable
        
    @property
    def speed(self):
        return self.resizable.scale_value(self.SPEED)
    
    def move(self, dx, dy, dt):
        self.ref_x += dx * self.speed * dt
        self.ref_y += dy * self.speed * dt
        self.ref_x = max(0, min(self.resizable.ref_field_size - self.ref_ragdoll_size, self.ref_x))
        self.ref_y = max(0, min(self.resizable.ref_field_size - self.ref_ragdoll_size, self.ref_y))

    def increase_satiety(self, amount):
        self.satiety = min(self.MAX_SATIETY, self.satiety + amount)

    def decrease_satiety(self, dt, decay_rate=6):
        self.satiety -= decay_rate * dt
        if self.satiety < 0:
            self.satiety = 0
            
    def is_overlapped(self, dx, dy):
        return self.cat_mask.overlap(self.treat_mask, (int(dx), int(dy)))
    