import pygame as pg
import pymunk.pygame_util
from pymunk import Vec2d


RES = WIDTH, HEIGHT = 800, 600
FPS = 60
MASS = 10
RADIUS = 10


pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
pymunk.pygame_util.positive_y_is_up = False
draw_options = pymunk.pygame_util.DrawOptions(surface)
space = pymunk.Space()
space.gravity = 0, 1000
floor = pymunk.Segment(
    space.static_body,
    Vec2d(0, HEIGHT - 10),
    Vec2d(WIDTH, HEIGHT - 10),
    10
)
floor.friction = 0.9
floor.elasticity = 0.9
space.add(floor)

ball_moment = pymunk.moment_for_circle(MASS, 0, RADIUS)

finished = False

while not finished:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEBUTTONDOWN:
            ball_body = pymunk.Body(MASS, ball_moment)
            ball_body.position = Vec2d(*event.pos)
            ball_shape = pymunk.Circle(
                ball_body,
                RADIUS
            )
            ball_shape.friction = 0.1
            ball_shape.elasticity = 0.9
            ball_shape.color = (255, 0, 0, 0)
            space.add(ball_body, ball_shape)

    dt = clock.tick(FPS)
    surface.fill(pg.Color('black'))
    space.step(dt / 1000)
    space.debug_draw(draw_options)
    pg.display.flip()

pg.quit()
