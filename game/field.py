import random

class GameField:
    MAX_TREATS = 3
    TREAT_LIFETIME = 6
    TREAT_MIN_DISTANCE = 100

    def __init__(self, width, height, treat_size):
        self.width = width
        self.height = height
        self.treat_size = treat_size 
        self._treats = []  

    def _spawn_treat(self, ragdoll, cat_mask, treat_mask):
        margin = self.treat_size // 2
        while True:
            x = random.randint(margin, self.width - self.treat_size - margin)
            y = random.randint(margin, self.height - self.treat_size - margin)
            if self._is_valid_treat_position(x,y, ragdoll, cat_mask, treat_mask):
                self._treats.append({'x': x, 'y': y, 'timer': 0.0})
                break
    def _is_valid_treat_position(self, x, y, ragdoll, cat_mask, treat_mask) -> bool:
        # check ragdoll
        offset = (int(x - ragdoll.x), int(y - ragdoll.y))
        distance = int((offset[0]**2 + offset[1]**2)**0.5)
        if cat_mask.overlap(treat_mask, offset) or distance < self.TREAT_MIN_DISTANCE:
            return False
        # check other treats
        for treat in self._treats:
            offset = (int(x - treat['x']), int(y - treat['y']))
            distance = int((offset[0]**2 + offset[1]**2)**0.5)
            if distance < self.TREAT_MIN_DISTANCE:
                return False
        return True

    def _despawn_treat(self, treat_item):
        if treat_item in self._treats:
            self._treats.remove(treat_item)

    def move_treats(self, ragdoll, cat_mask, treat_mask, dt):
        while len(self._treats) < self.MAX_TREATS:
            self._spawn_treat(ragdoll, cat_mask, treat_mask)
        for treat in self._treats:
            treat['timer'] += dt
            if treat['timer'] >= self.TREAT_LIFETIME:
                self._despawn_treat(treat)

    def collect_treats(self, ragdoll, cat_mask, treat_mask):
        count = 0
        for treat in self._treats:
            offset = (int(treat["x"] - ragdoll.x), int(treat["y"] - ragdoll.y))
            if cat_mask.overlap(treat_mask, offset):
                self._despawn_treat(treat)
                ragdoll.increase_satiety(20)
                count += 1
        return count
