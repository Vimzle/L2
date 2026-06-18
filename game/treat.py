import random

class Treat:
    def __init__(self, x, y, lifetime=0.0):
        self.ref_x = x # (0..FIELD_SIZE)
        self.ref_y = y
        self.timer = lifetime

class TreatManager:
    MAX_TREATS = 3
    TREAT_LIFETIME = 6
    TREAT_MIN_DISTANCE = 100

    def __init__(self, treat_size, resizable):
        self.ref_treat_size = treat_size 
        self.resizable = resizable
        self._treats = []  

    @property
    def treats(self):
        return list(self._treats)
    @staticmethod
    def _distance(x, o_x, y, o_y):
        dx = x - o_x
        dy = y - o_y
        return (dx**2 + dy**2)**0.5
        
    def _spawn_treat(self, ragdoll, ghost_manager):
        margin = self.ref_treat_size // 2
        while True:
            ref_x = random.randint(margin, self.resizable.ref_field_size - self.ref_treat_size - margin)
            ref_y = random.randint(margin, self.resizable.ref_field_size - self.ref_treat_size - margin)
            if self._is_valid_treat_position(ref_x,ref_y, ragdoll, ghost_manager):
                self._treats.append(Treat(ref_x, ref_y))
                break
    def _is_valid_treat_position(self, ref_x, ref_y, ragdoll, ghost_manager) -> bool:
        ghost = ghost_manager.ghost
        # check ghost
        # masks are based on scaled images -> use scaled coords
        if ghost is not None:
            dx_scaled = self.resizable.scale_value(ref_x - ghost.ref_x)
            dy_scaled = self.resizable.scale_value(ref_y - ghost.ref_y)
            if TreatManager._distance(ref_x, ghost.ref_x, ref_y, ghost.ref_y) < self.TREAT_MIN_DISTANCE or \
                ghost_manager.collides_with_treat(dx_scaled, dy_scaled):
                return False
        # check ragdoll
        dx_scaled = self.resizable.scale_value(ref_x - ragdoll.ref_x)
        dy_scaled = self.resizable.scale_value(ref_y - ragdoll.ref_y)
        if TreatManager._distance(ref_x, ragdoll.ref_x, ref_y, ragdoll.ref_y) < self.TREAT_MIN_DISTANCE or \
            ragdoll.collides_with_treat(dx_scaled, dy_scaled):
                return False
        # check treats
        for treat in self._treats:
            # TREAT_MIN_DISTANCE is in reference space -> use ref coords
            if TreatManager._distance(ref_x, treat.ref_x, ref_y, treat.ref_y) < self.TREAT_MIN_DISTANCE:
                return False
        return True

    def _despawn_treat(self, treat_item):
        if treat_item in self._treats:
            self._treats.remove(treat_item)

    def move_treats(self, ragdoll, ghost_manager, dt):
        while len(self._treats) < self.MAX_TREATS:
            self._spawn_treat(ragdoll, ghost_manager)
        for treat in self._treats[:]:
            treat.timer += dt
            if treat.timer >= self.TREAT_LIFETIME:
                self._despawn_treat(treat)

    def collect_treats(self, ragdoll):
        score = 0
        for treat in self._treats[:]:
            # masks are based on scaled images -> use scaled coords
            dx_scaled = self.resizable.scale_value(treat.ref_x - ragdoll.ref_x)
            dy_scaled = self.resizable.scale_value(treat.ref_y - ragdoll.ref_y)
            if ragdoll.collides_with_treat(dx_scaled, dy_scaled):
                self._despawn_treat(treat)
                score += 1
        return score
