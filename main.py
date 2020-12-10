import math

import pygame as pg
import pymunk.pygame_util
from pymunk import Vec2d

from tank import Tank, ball_radius


RES = WIDTH, HEIGHT = 800, 600
FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

pymunk.pygame_util.positive_y_is_up = False
draw_options = pymunk.pygame_util.DrawOptions(surface)
space = pymunk.Space()
space.gravity = 0, 500

fire_position = fire_x, fire_y = 50, 300


def create_building(space):
    size = 20
    mass = 10.0
    init_x = 500
    init_y = 200
    n_x = 10
    n_y = 10
    static_lines = [
        # horizontal
        pymunk.Segment(
            space.static_body,
            Vec2d(20, init_y + size * (n_y - 0.5)),
            Vec2d(init_x + n_x * 25, init_y + size * (n_y - 0.5)),
            10
        ),
        # vertical
        pymunk.Segment(
            space.static_body,
            Vec2d(init_x + n_x * 25, init_y),
            Vec2d(init_x + n_x * 25, init_y + size * (n_y - 0.5)),
            10
        ),
    ]
    for l in static_lines:
        l.friction = 0.9
        l.elasticity = 0.3
    space.add(*static_lines)

    boxes = []

    moment = pymunk.moment_for_box(mass, (size, size))
    for y in range(n_y):
        for x in range(0, n_x - n_y + y):
            body = pymunk.Body(mass, moment)
            body.position = Vec2d(
                init_x - y * size // 2 + x * size,
                init_y + y * size
            )
            shape = pymunk.Poly.create_box(body, (size, size))
            shape.elasticity = 0.5
            shape.friction = 0.5
            space.add(body, shape)
            boxes.append(body)
    return boxes


def main():
    balls = []
    boxes = create_building(space)
    tank = Tank(fire_x, fire_y, surface, space)

    while True:
        surface.fill(pg.Color('black'))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                balls.append(tank.fire(*event.pos))
            elif event.type == pg.MOUSEMOTION:
                tank.aim(*event.pos)

        space.step(1 / FPS)
        space.debug_draw(draw_options)

        [pg.draw.circle(surface, pg.Color('white'), (int(ball.position[0]), int(ball.position[1])),
                        ball_radius) for ball in balls]
        tank.draw()

        pg.display.flip()
        clock.tick(FPS)


try:
    main()
finally:
    pg.quit()
