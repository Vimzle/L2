import random

class Treat:
    def __init__(self, x, y, lifetime=0.0):
        self.x = x
        self.y = y
        self.timer = lifetime

class TreatManager:
    MAX_TREATS = 3
    TREAT_LIFETIME = 6
    TREAT_MIN_DISTANCE = 100

    def __init__(self, field_width, field_height, treat_size):
        self.field_width = field_width
        self.field_height = field_height
        self.treat_size = treat_size 
        self._treats = []  
    @property
    def treats(self):
        return list(self._treats)
    @staticmethod
    def _distance(x, o_x, y, o_y):
        dx = x - o_x
        dy = y - o_y
        return (dx**2 + dy**2)**0.5
        
    def _spawn_treat(self, ragdoll):
        margin = self.treat_size // 2
        while True:
            x = random.randint(margin, self.field_width - self.treat_size - margin)
            y = random.randint(margin, self.field_height - self.treat_size - margin)
            if self._is_valid_treat_position(x,y, ragdoll):
                self._treats.append(Treat(x, y))
                break
    def _is_valid_treat_position(self, x, y, ragdoll) -> bool:
        # check ragdoll
        if ragdoll.is_overlapped(x - ragdoll.x, y - ragdoll.y) or TreatManager._distance(x, ragdoll.x, y, ragdoll.y) < self.TREAT_MIN_DISTANCE:
            return False
        # check other treats
        for treat in self._treats:
            if TreatManager._distance(x, treat.x, y, treat.y) < self.TREAT_MIN_DISTANCE:
                return False
        return True

    def _despawn_treat(self, treat_item):
        if treat_item in self._treats:
            self._treats.remove(treat_item)

    def move_treats(self, ragdoll, dt):
        while len(self._treats) < self.MAX_TREATS:
            self._spawn_treat(ragdoll)
        for treat in self._treats:
            treat.timer += dt
            if treat.timer >= self.TREAT_LIFETIME:
                self._despawn_treat(treat)

    def collect_treats(self, ragdoll):
        score = 0
        for treat in self._treats:
            dx = treat.x - ragdoll.x
            dy = treat.y - ragdoll.y
            if ragdoll.is_overlapped(dx, dy):
                self._despawn_treat(treat)
                score += 1
        return score
