from typing import List

import pygame as pg
import pymunk.pygame_util
from pymunk import Vec2d

from explosion import Explosion
from tank import Tank

RES = WIDTH, HEIGHT = 800, 600
FPS = 60

tank_x, tank_y = 50, 300


def create_building(space: pymunk.Space) -> List[pymunk.Shape]:
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
    for line in static_lines:
        line.friction = 0.9
        line.elasticity = 0.3
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
            shape.collision_type = 10
            shape.ttl = 5
            shape.color = (255, 0, 0, 0)
            space.add(body, shape)
            boxes.append(shape)
    return boxes


def separate(arbiter, space, data):
    box, ball = arbiter.shapes
    if ball.body.velocity.get_length_sqrd() > 2000:
        ball.ttl -= 1
        box.ttl -= 1
        if box.ttl >= 0:
            box.color = (255 // 5 * box.ttl, 0, 0, 0)


def on_screen(box):
    l, b, r, t = box.bb
    return 0 < l < WIDTH and 0 < b < HEIGHT


def main():
    pg.init()
    surface = pg.display.set_mode(RES)
    clock = pg.time.Clock()

    pymunk.pygame_util.positive_y_is_up = False
    draw_options = pymunk.pygame_util.DrawOptions(surface)
    space = pymunk.Space()
    space.gravity = 0, 1000
    handler = space.add_collision_handler(10, 2)
    handler.separate = separate

    balls: List[pymunk.Shape] = []
    boxes = create_building(space)
    explosions: List[Explosion] = []
    tank = Tank(tank_x, tank_y, surface, space)

    while True:
        dt = clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                balls.append(tank.fire(*event.pos))
            elif event.type == pg.MOUSEMOTION:
                tank.aim(*event.pos)

        for box in boxes[:]:
            if box.ttl < 1 or not on_screen(box):
                space.remove(box, box.body)
                boxes.remove(box)

        for ball in balls[:]:
            if ball.ttl < 1 or not on_screen(ball):
                space.remove(ball, ball.body)
                balls.remove(ball)
                center = ball.body.position
                exp = Explosion(surface, center.x, center.y, 300)
                explosions.append(exp)

        for explosion in explosions[:]:
            explosion.update(dt)
            if not explosion.active:
                explosions.remove(explosion)

        surface.fill((77, 77, 77))
        space.step(1 / FPS)
        space.debug_draw(draw_options)

        if not boxes:
            font = pg.font.SysFont("Arial", 16)
            text = font.render('Congratulations!', True, pg.Color('white'))
            w = text.get_width()
            surface.blit(text, ((WIDTH - w) // 2, 20))

        tank.draw()
        for explosion in explosions:
            explosion.draw()

        pg.display.flip()


try:
    main()
finally:
    pg.quit()
