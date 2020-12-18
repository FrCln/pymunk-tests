import math
import os
from typing import Tuple

import pygame
import pymunk


ball_mass, ball_radius = 20, 7
impulse = 50


class Tank:
    x: float
    y: float
    color: Tuple[int, int, int]
    width: int
    height: int
    sprite: pygame.sprite.Sprite
    surface: pygame.surface.Surface
    power: float
    angle: float

    def __init__(self, x, y, surface, space, color=None):
        self.surface = surface
        self.space = space
        self.color = color
        self.y = y
        self.x = x
        self.angle = 0
        self.power = 10
        self.button_pressed = False
        self.max_power = 1000
        self.body_image = pygame.image.load(os.path.join('images', 'tank.png'))
        self.gun_image = pygame.image.load(os.path.join('images', 'gun.png'))
        self.width = self.body_image.get_width()
        self.height = self.body_image.get_height()

    def __repr__(self):
        return f'Tank({self.x}, {self.y}, {self.color}) power={self.power} angle={self.angle}'

    def aim(self, x, y):
        if y < self.y:
            self.angle = math.degrees(math.atan2(self.y - y, x - self.x)) - 90

    def fire(self, x, y) -> pymunk.shapes:
        dx = x - self.x
        dy = y - self.y
        imp_x = impulse * dx
        imp_y = impulse * dy
        ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
        ball_body = pymunk.Body(ball_mass, ball_moment)
        ball_body.position = self._calculate_gun_end()
        ball_body.apply_impulse_at_local_point((imp_x, imp_y), (0, 0))
        ball_shape = pymunk.Circle(ball_body, ball_radius)
        ball_shape.color = pygame.color.Color('white')
        ball_shape.elasticity = 0.5
        ball_shape.friction = 0.1
        ball_shape.collision_type = 2
        ball_shape.ttl = 1
        self.space.add(ball_body, ball_shape)
        return ball_shape

    def _calculate_gun_end(self):
        gun_size = self.gun_image.get_height()
        gun_x = self.x + self.gun_image.get_width()
        gun_y = self.y + self.gun_image.get_width() / 2
        x = gun_x - gun_size * math.sin(math.radians(self.angle))
        y = gun_y - gun_size * math.cos(math.radians(self.angle))
        return int(x), int(y)

    def draw(self):
        self.surface.blit(self.body_image, (int(self.x) - self.width // 2, int(self.y)))
        gun = pygame.transform.rotate(self.gun_image, self.angle)
        if self.angle < 0:
            gun_x = int(self.x)
        else:
            gun_x = int(self.x + self.gun_image.get_width() - gun.get_width())
        gun_y = int(self.y - gun.get_height() + self.gun_image.get_width() / 2)
        self.surface.blit(gun, (gun_x, gun_y))
