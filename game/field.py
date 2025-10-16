import random

class GameField:
    MAX_TREATS = 3
    TREAT_LIFETIME = 6

    def __init__(self, width, height, treat_size):
        self.width = width
        self.height = height
        # абстрактное "treat" для вариаций 
        self.treat_size = treat_size
        self._treats = []  

    def _generate_treat(self):
        margin = self.treat_size // 2
        x = random.randint(margin, self.width - self.treat_size - margin)
        y = random.randint(margin, self.height - self.treat_size - margin)
        self._treats.append({'x': x, 'y': y, 'timer': 0.0})

    def _remove_treat(self, treat_item):
        if treat_item in self._treats:
            self._treats.remove(treat_item)

    def move_treats(self, dt):
        while len(self._treats) < self.MAX_TREATS:
            self._generate_treat()
        for treat in self._treats:
            treat['timer'] += dt
            if treat['timer'] >= self.TREAT_LIFETIME:
                self._remove_treat(treat)

    def collect_treats(self, ragdoll, cat_mask, treat_mask):
        count = 0
        for treat in self._treats:
            offset = (int(treat["x"] - ragdoll.x), int(treat["y"] - ragdoll.y))
            if cat_mask.overlap(treat_mask, offset):
                self._remove_treat(treat)
                ragdoll.increase_satiety(20)
                count += 1
        return count
