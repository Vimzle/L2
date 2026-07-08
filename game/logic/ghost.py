import random

class Ghost:
    SPEED = 60
    GHOST_MIN_DISTANCE = 150
    def __init__(self, x, y):
        self.ref_x = x # (0..FIELD_SIZE)
        self.ref_y = y

class GhostManager():
    def __init__(self, ghost_size, ghost_mask, ragdoll, treat_manager, resizable):
        self.ref_ghost_size = ghost_size
        self.ghost_mask = ghost_mask 
        self.ragdoll = ragdoll
        self.treat_manager = treat_manager
        self.resizable = resizable
        self.ghost = None
        
    @property
    def speed(self):
        return self.resizable.scale_value(self.ghost.SPEED)
    
    @staticmethod
    def _distance(x, o_x, y, o_y):
        dx = x - o_x
        dy = y - o_y
        return (dx**2 + dy**2)**0.5
    
    def move(self, dt):
        distance = self._distance(self.ragdoll.ref_x, self.ghost.ref_x, self.ragdoll.ref_y, self.ghost.ref_y)
        if distance != 0:
            # direction vector v(x,y) (ghost -> ragdoll)
            # x: (self.ragdoll.ref_x - self.ghost.ref_x)
            # y: (self.ragdoll.ref_y - self.ghost.ref_y)
            # normalization -> v(x/|v|,y/|v|)
            dx = (self.ragdoll.ref_x - self.ghost.ref_x) / distance 
            dy = (self.ragdoll.ref_y - self.ghost.ref_y) / distance
            self.ghost.ref_x += dx * self.speed * dt
            self.ghost.ref_y += dy * self.speed * dt
            self.ghost.ref_x = max(0, min(self.resizable.ref_field_size - self.ref_ghost_size, self.ghost.ref_x))
            self.ghost.ref_y = max(0, min(self.resizable.ref_field_size - self.ref_ghost_size, self.ghost.ref_y))
        self.catch_ragdoll()

    def spawn_ghost(self):
        margin = self.ref_ghost_size // 2
        while True:
            ref_x = random.randint(margin, self.resizable.ref_field_size - self.ref_ghost_size - margin)
            ref_y = random.randint(margin, self.resizable.ref_field_size - self.ref_ghost_size - margin)
            if self._is_valid_ghost_position(ref_x,ref_y):
                self.ghost = Ghost(ref_x, ref_y)
                break

    def _is_valid_ghost_position(self, ref_x, ref_y) -> bool:
        # check ragdoll
        dx_scaled = self.resizable.scale_value(self.ragdoll.ref_x - ref_x)
        dy_scaled = self.resizable.scale_value(self.ragdoll.ref_y - ref_y)
        if GhostManager._distance(ref_x, self.ragdoll.ref_x, ref_y, self.ragdoll.ref_y) < Ghost.GHOST_MIN_DISTANCE or \
            self.collides_with_ragdoll(dx_scaled, dy_scaled):
            return False
        # check treats
        for treat in self.treat_manager._treats:
            # TREAT_MIN_DISTANCE is in reference space -> use ref coords
            if GhostManager._distance(ref_x, treat.ref_x, ref_y, treat.ref_y) < self.treat_manager.TREAT_MIN_DISTANCE:
                return False
        return True
    
    def catch_ragdoll(self):
        dx_scaled = self.resizable.scale_value(self.ragdoll.ref_x - self.ghost.ref_x)
        dy_scaled = self.resizable.scale_value(self.ragdoll.ref_y - self.ghost.ref_y)
        if self.collides_with_ragdoll(dx_scaled,dy_scaled):
            print("CATCHED!")
            self.ragdoll.is_catched = True

    def collides_with_treat(self, dx, dy):
        return self.ghost_mask.overlap(self.ragdoll.treat_mask, (int(dx), int(dy))) 
    def collides_with_ragdoll(self, dx,dy):
        return self.ghost_mask.overlap(self.ragdoll.cat_mask, (int(dx), int(dy))) 