import os

import pygame

sprites = [
    pygame.image.load(os.path.join('images', 'explosion', file))
    for file in sorted(os.listdir(os.path.join('images', 'explosion')))
    if file.startswith('explosion')
]


class Explosion:
    def __init__(self, surface: pygame.surface.Surface, x, y, time):
        """
        Create animation of explosion

        :param time: time in milliseconds
        """
        self.x = x
        self.y = y
        self.surface = surface
        self.sprite_num = 0
        self.time = time
        self.sprite_time = time / len(sprites)
        self.active = True
        self.cum_time = 0

    def update(self, dt):
        self.cum_time += dt
        self.sprite_num = int(self.cum_time / self.sprite_time)
        if self.sprite_num >= len(sprites):
            self.active = False
            return

    def draw(self):
        image = sprites[self.sprite_num]
        x = int(self.x - image.get_width() // 2)
        y = int(self.y - image.get_height() // 2)
        self.surface.blit(sprites[self.sprite_num], (x, y))
