import pygame

class Resizable:
    def __init__(self, ref_size, cur_size):
        self.ref_field_size = ref_size
        self.cur_field_size = cur_size
        self.scale = self.cur_field_size / ref_size

    def update(self, new_size):
        self.cur_field_size = new_size
        self.scale = self.cur_field_size / self.ref_field_size

    def scale_value(self, value):
        return value * self.scale
    
    def scale_image(self, original):
        return pygame.transform.scale(
            original, (int(original.get_width() * self.scale), int(original.get_height()*self.scale))
            )
    